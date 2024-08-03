from flask import jsonify, request, render_template, Blueprint
from flask_security import auth_required
from .models import db
from .extensions import datastore, bcrypt


authentication = Blueprint('authentication', __name__)

def check_user(email, password):
    # Check if email and password is provided
    if not email or not password: return jsonify({"message": "Email or Password not provided"}), 400
    # Check if email is valid
    user = datastore.find_user(email=email)
    if not user: return jsonify({"message": "Email or Password is incorrect"}), 400
    # Check password hash
    match = bcrypt.check_password_hash(user.password, password)
    if not match: return jsonify({"message": "Email or Password incorrect"}), 400
    # If everything is correct, return authentication token
    return {"token": user.get_auth_token(), "email": user.email, "role": str(user.roles[0].name)}, 200

@authentication.get('/api/auth/test')
def test():
    return jsonify({"message": "Authentication Service"}), 200

@authentication.post('/api/auth/login')
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    return check_user(email, password)

@authentication.post('/api/auth/register')
def register():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    role = data.get('role')
    if not email or not name or not password or not role: return jsonify({"message": "Essential Details missing"}), 400
    if role not in ["Sponsor", "Influencer"]: return jsonify({"message": "Invalid Role"}), 400
    user = datastore.find_user(email=email)
    if user: return jsonify({"message": "User Already Registered"}), 400
    reach = data.get('reach')
    category = data.get('category')
    industry = data.get('industry')
    if role == "Influencer" and (not reach or not category): return jsonify({"message": "Influencer Details missing"}), 400
    if role == "Sponsor" and not industry: return jsonify({"message": "Sponsor Details missing"}), 400
    user = datastore.create_user(email=email, name=name, password=bcrypt.generate_password_hash(password), active=True,
                                     industry=industry, category=category, reach=reach, roles=[role])
    db.session.add(user)

    db.session.commit()
    return jsonify({"token": user.get_auth_token(), "email": user.email, "role": role}), 201
