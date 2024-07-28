from flask_security import SQLAlchemyUserDatastore
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from .models import db, User, Role

bcrypt = Bcrypt()
cache = Cache()
datastore = SQLAlchemyUserDatastore(db, User, Role)

# Industry list for Sponsors
industries = [
    "Technology", "Finance", "Healthcare", "Education", "Manufacturing", "Retail", 
    "Real-Estate", "Entertainment", "Transportation", "Agriculture", "Automotive", 
    "Construction", "Energy", "Food-and-Beverage", "Hospitality", "Insurance", 
    "Media", "Pharmaceuticals", "Professional-Services", "Public-Sector", 
    "Telecommunications", "Utilities", "Logistics", "Mining", "Non-Profit", 
    "Aerospace", "Biotechnology", "Chemicals", "Consulting", "Defense", "Fashion", 
    "Furniture", "Human-Resources", "Legal", "Luxury-Goods", "Packaging", 
    "Publishing", "Recreation", "Security", "Sports", "Tourism", 
    "Waste-Management", "Wholesale"
]

# Category list for Influencers and Campaigns
categories = [
    "Beauty", "Fashion", "Fitness", "Health", "Travel", "Food", "Lifestyle", 
    "Gaming", "Technology", "Photography", "Music", "Parenting", "Finance", 
    "Education", "Sports", "Art", "Home-Decor", "Pets", "Automotive", "Books", 
    "DIY", "Environment", "Entertainment", "Business", "Spirituality", "Dating", 
    "Career", "Event-Planning", "Gaming-Cosplay", "Luxury", "Outdoors", 
    "Wellness", "Mental-Health", "Non-Profit", "Comedy", "News", 
    "Personal-Development", "Relationship", "Social-Justice", "Sustainable-Living", 
    "Tech-Gadgets", "Videography", "Yoga", "Crypto", "Investment", "Real-Estate"
]