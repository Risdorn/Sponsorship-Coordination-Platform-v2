from ..extensions import db
from ..models import Flagged, User
from .user import get_user

def get_flag(email):
    user = get_user(email=email)
    if not user: return {"message": "User Not Found"}
    flag = Flagged.query.filter_by(user_id=user.id).first()
    if not flag: return {"message": "User Not Flagged"}
    return flag

def flag_user(email, reason):
    user = get_user(email=email)
    if not user: return {"message": "User Not Found"}
    if "Admin" == user.role: return {"message": "Unauthorized"}
    flag = Flagged.query.filter_by(user_id=user.id).first()
    if flag: return {"message": "User Already Flagged"}
    flag = Flagged(user_id=user.id, reason=reason)
    db.session.add(flag)
    db.session.commit()
    return flag

def unflag_user(email):
    user = get_user(email=email)
    if not user: return {"message": "User Not Found"}, 400
    if "Admin" == user.role: return {"message": "Unauthorized"}, 401
    flag = Flagged.query.filter_by(user_id=user.id).first()
    if not flag: return {"message": "User Not Flagged"}, 400
    db.session.delete(flag)
    db.session.commit()
    return {"message": "User Unflagged Successfully"}, 200

def get_flagged_users(page):
    flags = Flagged.query.paginate(page, 10, False)
    user_ids = [flag.user_id for flag in flags.items]
    users = User.filter(User.id.in_(user_ids)).all()
    for i in range(len(users)):
        users[i].flag = True
        users[i].reason = flags.items[i].reason
    flags.items = users
    return flags