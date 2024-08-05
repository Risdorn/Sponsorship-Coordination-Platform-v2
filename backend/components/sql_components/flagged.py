from ..extensions import db
from ..models import Flagged, User
from .user import get_user

from datetime import date

def get_flag(email):
    user = get_user(email=email)
    if not user: return {"message": "User Not Found"}, False
    flag = Flagged.query.filter_by(type_id=user.id).first()
    if not flag: return {"message": "User Not Flagged"}, False
    return flag, True

def flag_user(email, reason):
    user = get_user(email=email)
    if not user: return {"message": "User Not Found"}, False
    if "Admin" == user.role: return {"message": "Unauthorized"}, False
    flag = Flagged.query.filter_by(type_id=user.id).first()
    if flag: return {"message": "User Already Flagged"}, False
    flag = Flagged(type_id=user.id, reason=reason, type="User", created_on=date.today())
    db.session.add(flag)
    db.session.commit()
    return flag, True

def unflag_user(email):
    user = get_user(email=email)
    if not user: return {"message": "User Not Found"}, 400
    if "Admin" == user.role: return {"message": "Unauthorized"}, 401
    flag = Flagged.query.filter_by(type_id=user.id).first()
    if not flag: return {"message": "User Not Flagged"}, 400
    db.session.delete(flag)
    db.session.commit()
    return {"message": "User Unflagged Successfully"}, 200

def get_flagged_users(page):
    flags = Flagged.query.paginate(page=page, per_page=5, error_out=False)
    user_ids = [flag.type_id for flag in flags.items]
    users = User.query.filter(User.id.in_(user_ids)).all()
    for i in range(len(users)):
        users[i].flag = True
        users[i].reason = flags.items[i].reason
        users[i].role = users[i].roles[0].name
    flags.items = users
    return flags