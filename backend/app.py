from flask import Flask
from flask_security import Security, auth_required
from flask_cors import CORS
from redis import Redis
from celery.schedules import crontab
from celery.result import AsyncResult
import logging

from components.extensions import bcrypt, datastore, cache
from components.celery_worker import celery_init_app
from components.celery_jobs import daily_reminder, send_monthly_report, create_resource_csv
from components.models import db
from components.api import api
from components.authentication import authentication
from config import DevelopmentConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    app.security = Security(app, datastore)
    db.init_app(app)
    bcrypt.init_app(app)
    api.init_app(app)
    app.register_blueprint(authentication)
    
    # CORS for separate servers
    CORS(app)
    
    # Initialize Flask-Caching with Redis
    cache.init_app(app)

    # Initialize Redis client
    redis_client = Redis(host='localhost', port=6379, db=0)
    
    return app

app = create_app()
celery = celery_init_app(app)

@celery.on_after_configure.connect
def automated_tasks(sender, **kwargs):
    logger.info("Setting up automated tasks")
    # daily reminder, given at 6:00 AM
    sender.add_periodic_task(
        #crontab(hour=0,minute=20),
        30,
        daily_reminder.s(),
    )
    logger.info("Daily reminder task set up at time")
    # monthly report, given at 12:01 AM on the first day of the month
    sender.add_periodic_task(
        #crontab(day_of_month=1, hour=0, minute=1),
        30,
        send_monthly_report.s(),
    )
    logger.info("Monthly report task set up")

# Manual trigger for all celery tasks
@app.route('/trigger_daily_reminder')
@auth_required('token')
def trigger_daily_reminder():
    daily_reminder.delay()
    return 'Daily reminder triggered!'

@app.route('/trigger_monthly_report')
@auth_required('token')
def trigger_monthly_report():
    send_monthly_report.delay()
    return 'Monthly report triggered!'

@app.route('/trigger_create_resource_csv/<int:id>')
@auth_required('token')
def trigger_create_resource_csv(id):
    result = create_resource_csv.delay(id)
    # Check the status of the task
    task_id = result.id
    print(f"Task ID: {task_id}")

    # Get the result of the task
    result = AsyncResult(task_id)
    print(f"Task Status: {result.status}")
    if result.status == 'SUCCESS':
        print(f"Task Result: {result.result}")
    return 'Create resource CSV triggered!'



if __name__ == '__main__':
    print(app.url_map)
    app.run()