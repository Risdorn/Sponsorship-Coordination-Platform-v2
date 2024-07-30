from ..models import db, Ad_request
from .campaign import get_campaign
from datetime import date
import re

def validate_ad_request(campaign_id, messages, requirements, payment_amount, status = None):
    # Check if all fields are filled
    if not messages or not requirements or not payment_amount: return False, "All fields are required"
    # Check if messages, requirements are not too long
    if len(messages) > 250 or len(requirements) > 250: return False, "Messages and Requirements should be less than 250 characters"
    # Check if payment amount is a number
    if not re.search(r'^\d+(\.\d+)?$', payment_amount): return False, "Payment amount should be a number"
    # Check if Payment Amount is greater than remaining budget
    campaign = get_campaign(campaign_id)
    if not campaign: return False, "Invalid Campaign ID"
    if float(payment_amount) > campaign.remianing: return False, "Payment amount is greater than remaining budget"
    # Check if status is valid
    if status and status not in ["Pending", "Accept", "Reject"]: return False, "Invalid status"
    return True, ""

def validate_update_ad(ad_request_id, messages, requirements, payment_amount):
    ad_request = get_ad_request(ad_request_id)
    if not ad_request: return False, "Invalid Ad Request ID"
    # Ad Request can only be updated if it is pending and not in negotiation
    if ad_request.status != "Pending" or ad_request.negotiate: return False, "Ad Request cannot be changed"
    # Check if all fields are filled
    if len(messages) > 250 or len(requirements) > 250: return False, "Messages and Requirements should be less than 250 characters"
    # Check if payment amount is a number
    if not re.search(r'^\d+(\.\d+)?$', payment_amount): return False, "Payment amount should be a number"
    return True, ""

def validate_revert_ad(ad_request_id, status):
    ad_request = get_ad_request(ad_request_id)
    if not ad_request: return False, "Invalid Ad Request ID"
    # Ad Request can only be reverted if it is accepted or rejected
    if status not in ["Accept", "Reject"]: return False, "Invalid status"
    # If status is Accept, check if payment amount is greater than remaining budget
    campaign = get_campaign(ad_request.campaign_id)
    if status == "Accept" and ad_request.payment_amount > campaign.remaining: return False, "Payment amount is greater than remaining budget"
    return True, ""

def validate_negotiate_ad(ad_request_id, payment_amount):
    ad_request = get_ad_request(ad_request_id)
    if not ad_request: return False, "Invalid Ad Request ID"
    # Ad Request can only be negotiated if it is Pending
    if ad_request.status != "Pending": return False, "Ad Request cannot be negotiated"
    # Check if payment amount is a number
    if not re.search(r'^\d+(\.\d+)?$', payment_amount): return False, "Payment amount should be a number"
    # Check if Payment Amount is greater than remaining budget
    campaign = get_campaign(ad_request.campaign_id)
    if float(payment_amount) > campaign.remaining: return False, "Payment amount is greater than remaining budget"
    return True, ""

def create_ad_request(messages, requirements, payment_amount, status, negotiate, campaign_id, influencer_id = None):
    # Create ad request
    # Influencer_id is optional, empty ad requests which will be filled by influencers
    created = date.today()
    ad_request = Ad_request(campaign_id=campaign_id, influencer_id=influencer_id, messages=messages, requirements=requirements,
                            payment_amount=payment_amount, status=status, negotiate=negotiate, created_on=created)
    db.session.add(ad_request)
    db.session.commit()
    return ad_request

def get_ad_request(ad_request_id):
    # Get ad request
    ad_request = Ad_request.query.filter_by(id=ad_request_id).first()
    return ad_request

def update_ad_request(ad_request_id, params):
    # Update ad request
    ad_request = get_ad_request(ad_request_id)
    for key in params:
        if not params[key]: continue
        if key == "status" and params[key] == "Accept":
            ad_request.accepted_on = date.today()
            campaign = get_campaign(ad_request.campaign_id)
            campaign.remaining -= ad_request.payment_amount
        elif key == "status" and params[key] == "Reject":
            ad_request.rejected_on = date.today()
        setattr(ad_request, key, params[key])
    db.session.commit()
    return ad_request

def delete_ad_request(ad_request_id):
    # Delete ad request
    ad_request = get_ad_request(ad_request_id)
    db.session.delete(ad_request)
    db.session.commit()
    return ad_request

def get_campaign_ad_requests(campaign_id, page):
    # Get ad requests associated with campaign
    ad_requests = Ad_request.query.filter_by(campaign_id=campaign_id).paginate(page=page, per_page=5, error_out=False)
    ad_requests.pages_iter = []
    for page in ad_requests.iter_pages():
        ad_requests.pages_iter.append(page)
    return ad_requests

def get_influencer_ad_requests(influencer_id, page):
    # Get ad requests associated with influencer
    ad_requests = Ad_request.query.filter_by(influencer_id=influencer_id).paginate(page=page, per_page=5, error_out=False)
    ad_requests.pages_iter = []
    for page in ad_requests.iter_pages():
        ad_requests.pages_iter.append(page)
    return ad_requests

def get_all_ad_requests(page):
    # Get all ad requests
    ad_requests = Ad_request.query.paginate(page=page, per_page=5, error_out=False)
    ad_requests.pages_iter = []
    for page in ad_requests.iter_pages():
        ad_requests.pages_iter.append(page)
    return ad_requests