from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery.utils.log import get_task_logger
from celery import shared_task
from jinja2 import Template
import csv
from datetime import date
from flask import url_for

from .models import User, Role, Campaign, Ad_request
from .graphs import encode_image, ad_request_month_status, payment_distribution_month

SMTP_HOST = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = 'donot-reply@reminders.com'
SENDER_PASSWORD = ''

# Function to send reports
def send_message(to, subject, content_body):
    msg = MIMEMultipart()
    msg["To"] = to
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg.attach(MIMEText(content_body, 'html'))
    try: 
        client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
        client.send_message(msg=msg)
        client.quit()
    except Exception as e:
        logger.error("Error sending email: %s", e)

logger = get_task_logger(__name__)


@shared_task(ignore_result=False)
def create_resource_csv(sponsor_id):
    logger.info("Creating CSV for sponsor %s", sponsor_id)
    campaigns = Campaign.query.with_entities(
        Campaign.id.label('Id'), 
        Campaign.name.label('Name'), 
        Campaign.description.label('Description'), 
        Campaign.start_date.label('Start Date'), 
        Campaign.end_date.label('End Date'), 
        Campaign.category.label('Category'),
        Campaign.budget.label('Budget'), 
        Campaign.visibility.label('Visibility'), 
        Campaign.goals.label('Goals'), 
        Campaign.remaining.label('Remaining budget'), 
        Campaign.created_on.label('Created On')
    ).filter_by(sponsor_id=sponsor_id).all()

    campaigns = [campaign._asdict() for campaign in campaigns]
    field_name = ["Id", "Name", "Description", "Start Date", "End Date", "Category", "Budget", "Visibility", "Goals", "Remaining budget", "Created On"]
    
    logger.info("Creating CSV of length %s", len(campaigns))
    
    filename = "static/campaigns.csv"

    with open(filename, 'w', newline='') as f:
        logger.info("Writing CSV to file")
        writer = csv.DictWriter(f, fieldnames=field_name)
        writer.writeheader()
        writer.writerows(campaigns)
    #file_url = url_for('static', filename=filename, _external=True)
    return filename


@shared_task(ignore_result=True)
def daily_reminder():
    logger.info("Sending daily reminders")
    users = User.query.filter(User.roles.any(Role.name == "Influencer")).all()
    logger.info("Found %s influencers", len(users))
    for user in users:
        pending_ads = Ad_request.query.filter_by(influencer_id=user.id, status="Pending", negotiate=False).count()
        logger.info("Sending daily reminder to %s", user.email)
        logger.info("Pending ads: %s", pending_ads)
        if pending_ads >= 0:
            with open('static/daily_reminder.html', 'r') as f:
                logger.info("Sending daily reminder to %s", user.email)
                template = Template(f.read())
                send_message(user.email, "You have pending ads", template.render(name=user.name, pending_ads=pending_ads))
    return "OK"



@shared_task(ignore_result=True)
def send_monthly_report():
    logger.info("Sending monthly reports")
    users = User.query.filter(User.roles.any(Role.name == 'Sponsor')).all()
    logger.info("Found %s sponsors", len(users))
    for user in users:
        total_campaigns = Campaign.query.filter_by(sponsor_id=user.id).filter(Campaign.created_on < date.today())
        total_campaigns = total_campaigns.filter(Campaign.created_on > date.today().replace(month=date.today().month - 1)).count()
        campaign_ids = [campaign.id for campaign in Campaign.query.filter_by(sponsor_id=user.id).all()]
        total_ads = Ad_request.query.filter(Ad_request.campaign_id.in_(campaign_ids))
        total_ads = total_ads.filter(Ad_request.created_on < date.today()).filter(Ad_request.created_on > date.today().replace(month=date.today().month - 1)).count()
        ad_request_graph = encode_image(ad_request_month_status(user.id))
        payment_graph = encode_image(payment_distribution_month(user.id))
        logger.info("Sending monthly report to %s", user.email)
        with open('static/monthly_report.html', 'r') as f:
            template = Template(f.read())
            logger.info("Sending monthly report to %s", user.email)
            send_message(user.email, "Monthly Report",
                         template.render(ad_request_graph=ad_request_graph, payment_graph=payment_graph, name=user.name,
                                         total_campaigns=total_campaigns, total_ads=total_ads))
    return "OK"