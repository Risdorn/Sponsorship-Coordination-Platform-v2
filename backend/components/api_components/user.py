from flask_restful import Resource, reqparse, fields, marshal
from flask_security import auth_required

from ..sql_components.user import *
from ..sql_components.flagged import *
from ..graphs import *

user_marshal = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "role": fields.String,
    "industry": fields.String,
    "category": fields.String,
    "reach": fields.Integer,
    "flag": fields.Boolean,
    "reason": fields.String,
    "created_on": fields.String
}

flag_marshal = {
    "id": fields.Integer,
    "type_id": fields.Integer,
    "reason": fields.String,
    "type": fields.String,
    "created_on": fields.String
}

pagination_marshal = {
    "total": fields.Integer,
    "per_page": fields.Integer,
    "page": fields.Integer,
    "pages_iter": fields.List(fields.Integer),
    "has_next": fields.Boolean,
    "has_prev": fields.Boolean,
    "next_num": fields.Integer,
    "prev_num": fields.Integer,
    "items": fields.List(fields.Nested(user_marshal))
}

user_parser = reqparse.RequestParser()
user_parser.add_argument("name", location="json")
user_parser.add_argument("email", location="json")
user_parser.add_argument("password", location="json")
user_parser.add_argument("confirm_password", location="json")
user_parser.add_argument("industry", location="json")
user_parser.add_argument("category", location="json")
user_parser.add_argument("reach", location="json")

search_parser = reqparse.RequestParser()
search_parser.add_argument("name", help="Search for users with name like", location="json")
search_parser.add_argument("sort", help="Ascending or Descending", location="json")
search_parser.add_argument("category", help="Filter By Category", location="json")
search_parser.add_argument("page", help="Page Number", location="json")

flag_parser = reqparse.RequestParser()
flag_parser.add_argument("reason", location="json")

class Users(Resource):
    @auth_required('token')
    def get(self, email):
        user = get_user(email=email)
        if not user: return {"message": "User Not Found"}, 400
        if "Admin" == user.role: return {"message": "Unauthorized"}, 401
        flag, valid = get_flag(email)
        if not valid: user.flag = False
        else: 
            user.flag = True
            user.reason = flag.reason
        return marshal(user, user_marshal), 200
    
    @auth_required('token')
    def put(self, email):
        args = user_parser.parse_args()
        valid, message = validate_update_user(email, args.get('name'), args.get('password'), args.get('industry'), args.get('category'), args.get('reach'))
        if not valid: return {"message": message}, 400
        user = update_user(email, {"name": args.get('name'), "password": args.get('password'), "industry": args.get('industry'), 
                                     "category": args.get('category'), "reach": args.get('reach')})
        return marshal(user, user_marshal), 200
    
    @auth_required('token')
    def delete(self, email):
        user = get_user(email=email)
        if not user: return {"message": "User Not Found"}, 400
        flag, valid = get_flag(email)
        if valid: unflag_user(email)
        delete_user(email)
        return {"message": "User Deleted Successfully"}, 200
    
    def post(self): return {"message": "POST not allowed"}, 405

class Search_Influencer(Resource):
    @auth_required('token')
    def post(self):
        args = search_parser.parse_args()
        users = search_user(args.get('name'), args.get('sort'), args.get('category'), int(args.get('page', 1)))
        for user in users.items:
            flag, valid = get_flag(user.email)
            if not valid: user.flag = False
            else: 
                user.flag = True
                user.reason = flag.reason
        return marshal(users, pagination_marshal), 200
    
    def get(self): return {"message": "GET not allowed"}, 405
    def put(self): return {"message": "PUT not allowed"}, 405
    def delete(self): return {"message": "DELETE not allowed"}, 405
    
class All_Users(Resource):
    @auth_required('token')
    def post(self):
        args = search_parser.parse_args()
        users = get_all_users(int(args.get('page', 1)))
        for user in users.items:
            flag, valid = get_flag(user.email)
            if not valid: user.flag = False
            else: 
                user.flag = True
                user.reason = flag.reason
        return marshal(users, pagination_marshal), 200
    
    def get(self): return {"message": "GET not allowed"}, 405
    def put(self): return {"message": "PUT not allowed"}, 405
    def delete(self): return {"message": "DELETE not allowed"}, 405

class Flag_User(Resource):
    @auth_required('token')
    def get(self, email):
        response, valid = get_flag(email)
        if not valid: return response, 400
        return marshal(response, flag_marshal), 200
    
    @auth_required('token')
    def post(self, email):
        args = flag_parser.parse_args()
        if not args.get('reason'): return {"message": "Reason is required"}, 400
        flag, valid = flag_user(email, args.get('reason'))
        if not valid: return flag, 400
        return marshal(flag, flag_marshal), 200
    
    @auth_required('token')
    def delete(self, email):
        return unflag_user(email)
    
    def put(self): return {"message": "PUT not allowed"}, 405

class Flagged_Users(Resource):
    @auth_required('token')
    def post(self):
        args = search_parser.parse_args()
        users = get_flagged_users(int(args.get('page', 1)))
        return marshal(users, pagination_marshal), 200
    
    def get(self): return {"message": "GET not allowed"}, 405
    def put(self): return {"message": "PUT not allowed"}, 405
    def delete(self): return {"message": "DELETE not allowed"}, 405

class get_Stats(Resource):
    @auth_required('token')
    @cache.memoize(timeout=3600)
    def get(self, email):
        key = f"stats_{email}"
        if cache.get(key): return cache.get(key)
        user = get_user(email=email)
        if not user: return {"message": "User Not Found"}, 400
        data = {}
        data['user'] = marshal(user, user_marshal)
        data["user_over_time"] = encode_image(user_over_time())
        data["campaigns_over_time"] = encode_image(campaigns_over_time(user.id))
        data["ad_requests_over_time"] = encode_image(ad_request_over_time(user.id, user.role.lower()))
        data["ad_request_status"] = encode_image(ad_request_status_distribution(user.id, user.role.lower()))
        data["payment_distribution"] = encode_image(payment_amount_distribution(user.id, user.role.lower()))
        cache.set(key, data)
        return data, 200