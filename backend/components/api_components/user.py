from flask import jsonify
from flask_restful import Resource, reqparse, fields, marshal
from flask_security import auth_required

from ..sql_components.user import *

user_marshal = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "role": fields.String,
    "industry": fields.String,
    "category": fields.String,
    "reach": fields.Integer,
    "created_on": fields.String
}

user_parser = reqparse.RequestParser()
user_parser.add_argument("name", location="form")
user_parser.add_argument("email", location="form")
user_parser.add_argument("password", location="form")
user_parser.add_argument("industry", location="form")
user_parser.add_argument("category", location="form")
user_parser.add_argument("reach", location="form")

search_parser = reqparse.RequestParser()
search_parser.add_argument("name", help="Search for users with name like", location="form")
search_parser.add_argument("reach", help="Ascending or Descending", location="form")
search_parser.add_argument("category", help="Filter By Category", location="form")

class Users(Resource):
    @auth_required('token')
    def get(self, user_id):
        user = get_user(id=user_id)
        if not user: return {"message": "User Not Found"}, 400
        if "Admin" in user.roles: return {"message": "Unauthorized"}, 401
        return marshal(user, user_marshal), 200
    
    @auth_required('token')
    def put(self, user_id):
        args = user_parser.parse_args()
        valid, message = validate_update_user(user_id, args.get('name'), args.get('password'), args.get('industry'), args.get('category'), args.get('reach'))
        if not valid: return {"message": message}, 400
        user = update_user(user_id, {"name": args.get('name'), "password": args.get('password'), "industry": args.get('industry'), 
                                     "category": args.get('category'), "reach": args.get('reach')})
        return marshal(user, user_marshal), 200
    
    @auth_required('token')
    def delete(self, user_id):
        args = user_parser.parse_args()
        if not args.get('email') or not args.get('password'): return {"message": "Email and Password are required"}, 400
        user = validate_user(args.get('email'), args.get('password'))
        if not user: return {"message": "Invalid Credentials"}, 400
        if "Admin" != user.role: return {"message": "Unauthorized"}, 401
        user = get_user(id=user_id)
        if not user: return {"message": "User Not Found"}, 400
        delete_user(user_id)
        return {"message": "User Deleted Successfully"}, 200
    
    def post(self): return {"message": "POST not allowed"}, 405

class Search_Influencer(Resource):
    @auth_required('token')
    def post(self):
        args = search_parser.parse_args()
        users = search_user(args.get('name'), args.get('reach'), args.get('category'))
        for i in range(len(users)):
            users[i] = marshal(users[i], user_marshal)
        return users, 200
    
    def get(self): return {"message": "GET not allowed"}, 405
    def put(self): return {"message": "PUT not allowed"}, 405
    def delete(self): return {"message": "DELETE not allowed"}, 405