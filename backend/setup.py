from app import app
from components.extensions import datastore, bcrypt
from components.models import db, Role

with app.app_context():
    db.drop_all()
    db.create_all()
    # Creating Roles
    datastore.find_or_create_role(name="Admin", description="Admins have control over everything")
    datastore.find_or_create_role(name="Sponsor", description="Sponsors can create Campaigns and Ad Requests")
    datastore.find_or_create_role(name="Influencer", description="Influencers can respond to Ad Requests")
    db.session.commit()
    # Create a User for each role
    if not datastore.find_user(email="admin@gmail.com"):
        datastore.create_user(name="Admin", email="admin@gmail.com", password=bcrypt.generate_password_hash("Admin@12"), roles=["Admin"])
        
    if not datastore.find_user(email="sponsor1@gmail.com"):
        datastore.create_user(name="Sponsor_1", email="sponsor1@gmail.com", password=bcrypt.generate_password_hash("Sponsor@1"), roles=["Sponsor"], active=True)
    
    if not datastore.find_user(email="influencer1@gmail.com"):
        datastore.create_user(name="Influencer_1", email="influencer1@gmail.com", password=bcrypt.generate_password_hash("Influencer@1"), roles=["Influencer"], active=True)
    
    if not datastore.find_user(email="influencer2@gmail.com"):
        datastore.create_user(name="Influencer_2", email="influencer2@gmail.com", password=bcrypt.generate_password_hash("Influencer@2"), roles=["Influencer"], active=True)
    
    db.session.commit()
