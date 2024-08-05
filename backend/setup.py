from app import app, db
from components.extensions import datastore, bcrypt
#from components.models import db
from fake_data import generate_sample_data

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
    
    generate_sample_data(db)
    
    db.session.commit()
