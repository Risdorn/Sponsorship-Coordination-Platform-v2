from flask_restful import Resource, reqparse, fields, marshal
from flask_security import auth_required

from ..sql_components.ad_request import *

ad_request_marshal = {
    "id": fields.Integer,
    "influencer_id": fields.Integer,
    "campaign_id": fields.Integer,
    "messages": fields.String,
    "requirements": fields.String,
    "payment_amount": fields.Float,
    "status": fields.String,
    "negotiate": fields.Boolean,
    "created_on": fields.String,
    "accepted_on": fields.String,
    "rejected_on": fields.String,
    "campaign": fields.Nested({
        "name": fields.String,
    }),
    "influencer": fields.Nested({
        "name": fields.String,
    })
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
    "items": fields.List(fields.Nested(ad_request_marshal))
}

ad_request_parser = reqparse.RequestParser()
ad_request_parser.add_argument("influencer_id", location="json")
ad_request_parser.add_argument("campaign_id", location="json")
ad_request_parser.add_argument("messages", location="json")
ad_request_parser.add_argument("requirements", location="json")
ad_request_parser.add_argument("payment_amount", location="json")

search_parser = reqparse.RequestParser()
search_parser.add_argument("influencer_id", help="Get all ad requests associated with Influencer", location="json")
search_parser.add_argument("campaign_id", help="Get all ad requests associated with Campaign", location="json")
search_parser.add_argument("page", help="Page Number", location="json")

class Ad_requests(Resource):
    @auth_required('token')
    def get(self, ad_request_id):
        ad_request = get_ad_request(ad_request_id)
        if not ad_request: return {"message": "Invalid Ad Request ID"}, 400
        return marshal(ad_request, ad_request_marshal), 200
    
    @auth_required('token')
    def put(self, ad_request_id):
        args = ad_request_parser.parse_args()
        valid, message = validate_update_ad(ad_request_id, args.get('messages'), args.get('requirements'), args.get('payment_amount'))
        if not valid: return {"message": message}, 400
        ad_request = update_ad_request(ad_request_id, {"messages": args.get('messages'), "requirements": args.get('requirements'), 
                                                       "payment_amount": args.get('payment_amount')})
        return marshal(ad_request, ad_request_marshal), 200
    
    @auth_required('token')
    def delete(self, ad_request_id):
        ad_request = get_ad_request(ad_request_id)
        if not ad_request: return {"message": "Invalid Ad Request ID"}, 400
        if ad_request.status != "Pending": return {"message": "Ad Request cannot be deleted"}, 400
        delete_ad_request(ad_request_id)
        return {"message": "Ad Request deleted successfully"}, 200
    
    def post(self): return {"message": "POST not allowed"}, 405

class Create_Ad_Request(Resource):
    @auth_required('token')
    def post(self):
        args = ad_request_parser.parse_args()
        if not args.get('campaign_id'): return {"message": "Campaign ID is required"}, 400
        valid, message = validate_ad_request(args.get('campaign_id'), args.get('messages'), args.get('requirements'), args.get('payment_amount'), 'Pending')
        if not valid: return {"message": message}, 400
        ad_request = create_ad_request(args.get('messages'), args.get('requirements'), args.get('payment_amount'), 'Pending', False, args.get('campaign_id'),
                                       args.get('influencer_id'))
        return marshal(ad_request, ad_request_marshal), 201
    
    def get(self): return {"message": "GET not allowed"}, 405
    def put(self): return {"message": "PUT not allowed"}, 405
    def delete(self): return {"message": "DELETE not allowed"}, 405

class Revert_Ad_Request(Resource):
    @auth_required('token')
    def put(self, ad_request_id):
        args = ad_request_parser.parse_args()
        valid, message = validate_revert_ad(ad_request_id, args.get('status'))
        if not valid: return {"message": message}, 400
        ad_request = update_ad_request(ad_request_id, {"status": args.get('status'), "negotiate": True})
        return marshal(ad_request, ad_request_marshal), 200
    
    def post(self): return {"message": "POST not allowed"}, 405
    def get(self): return {"message": "GET not allowed"}, 405
    def delete(self): return {"message": "DELETE not allowed"}, 405

class Negotiate_Ad_Request(Resource):
    @auth_required('token')
    def put(self, ad_request_id):
        args = ad_request_parser.parse_args()
        valid, message = validate_negotiate_ad(ad_request_id, args.get('payment_amount'))
        if not valid: return {"message": message}, 400
        ad_request = update_ad_request(ad_request_id, {"payment_amount": args.get('payment_amount'), "negotiate": True})
        return marshal(ad_request, ad_request_marshal), 200
    
    def post(self): return {"message": "POST not allowed"}, 405
    def get(self): return {"message": "GET not allowed"}, 405
    def delete(self): return {"message": "DELETE not allowed"}, 405

class All_Ad_Requests(Resource):
    @auth_required('token')
    def post(self):
        args = ad_request_parser.parse_args()
        args['page'] = int(args.get('page', 1))
        if args.get('influencer_id'): ad_requests = get_influencer_ad_requests(args.get('influencer_id'), args.get('page'))
        elif args.get('campaign_id'): ad_requests = get_campaign_ad_requests(args.get('campaign_id'), args.get('page'))
        elif args.get('sponsor_id'): ad_requests = get_sponsor_ad_requests(args.get('sponsor_id'), args.get('page'))
        else: ad_requests = get_all_ad_requests(args.get('page'))
        return marshal(ad_requests, pagination_marshal), 200
    
    def get(self): return {"message": "GET not allowed"}, 405
    def put(self): return {"message": "PUT not allowed"}, 405
    def delete(self): return {"message": "DELETE not allowed"}, 405