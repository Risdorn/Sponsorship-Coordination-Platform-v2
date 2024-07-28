from ..extensions import bcrypt, industries, categories
from ..models import db, User
from datetime import date
import re

def validate_form(name, email, password, con_pass, role, reach = None, industry = None, category = None):
    # Make sure all fields are filled
    if not name or not email or not password or not con_pass or not role: return False, "All fields are required"
    # Make sure password and confirm password match
    if password != con_pass: return False, "Passwords do not match"
    # Make sure name is not too long
    if len(name) > 45: return False, "Name should be less than 45 characters"
    # For Influencers, make sure reach and category is provided
    # Reach should be a number and category should be valid
    if role == "Influencer" and (not reach or not category): return False, "Reach and Category are required"
    if role == "Influencer" and category not in categories: return False, "Invalid category"
    if role == "Influencer" and not re.search(r'^\d+$', reach): return False, "Reach should be a number"
    # For Sponsors, make sure industry is provided
    # Industry should be valid
    if role == "Sponsor" and not industry: return False, "Industry is required"
    if role == "Sponsor" and industry not in industries: return False, "Invalid industry"
    # For all users, make sure name, email and password is valid
    name = re.search(r'^[\w\-\s]+$', name)
    email = re.search(r'^[\w\.\-]+@[\w\.\-]+\.\w+$', email)
    password = re.search(r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?!.* ).{8,}$', password)
    if not name or not email or not password: return False, "Invalid format"
    return True, ""

def validate_update_user(user_id, name, password, industry, category, reach):
    # Make sure user exists
    user = get_user(id=user_id)
    if not user: return False, "Invalid User ID"
    # Make sure name is not too long
    if name and len(name) > 45: return False, "Name should be less than 45 characters"
    # Reach should be a number and category should be valid
    if "Influencer" in user.roles and category and category not in categories: return False, "Invalid category"
    if "Influencer" in user.roles and reach and not re.search(r'^\d+$', reach): return False, "Reach should be a number"
    # Industry should be valid
    if "Sponsor" in user.roles and industry and industry not in industries: return False, "Invalid industry"
    # For all users, make sure name and password is valid
    if name:
        name = re.search(r'^[\w\-\s]+$', name)
        if not name: return False, "Invalid name"
    if password:
        password = re.search(r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?!.* ).{8,}$', password)
        if not password: return False, "Invalid password"
    return True, ""

def validate_user(email, password):
    # Check if user exists
    user = get_user(email)
    if not user: return None
    # Check if password is correct
    if not bcrypt.check_password_hash(user.password, password): return None
    return user

def create_user(name, email, password, role, industry = None, category = None, reach = None):
    # Create user
    created = date.today()
    password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(name=name, email=email, password=password, industry=industry, category=category, reach=reach, roles=[role], created_on=created)
    db.session.add(user)
    db.session.commit()
    return user

def get_user(email, id = None):
    # Get user
    # If id is provided, get user by id
    if id: return User.query.filter_by(id=id).first()
    user = User.query.filter_by(email=email).first()
    return user

def update_user(email, params):
    # Update user
    user = get_user(email)
    for key in params:
        if not params[key]: continue
        if key == "password":
            params[key] = bcrypt.generate_password_hash(params[key]).decode('utf-8')
        setattr(user, key, params[key])
    db.session.commit()
    return user

def delete_user(email):
    # Delete user
    user = get_user(email)
    db.session.delete(user)
    db.session.commit()
    return user

def search_user(name, reach, category):
    users = User.query.filter(User.roles.any("Influencer"))
    if category: users = users.filter_by(category=category)
    if name: users = users.filter(User.name.like('%' + name + '%'))
    # Sort based on reach
    if reach == "Descending":
        users = users.order_by(User.reach.desc())
    elif reach == "Ascending":
        users = users.order_by(User.reach.asc())
    return users.all()
        