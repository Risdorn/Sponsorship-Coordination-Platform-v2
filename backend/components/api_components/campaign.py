from flask_restful import Resource, reqparse, fields, marshal
from flask_security import auth_required

from ..sql_components.campaign import *
from ..sql_components.ad_request import get_campaign_ad_requests, delete_ad_request
from ..sql_components.user import get_user

campaign_marshal = {
    "id": fields.Integer,
    "sponsor_id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "visibility": fields.String,
    "goals": fields.String,
    "category": fields.String,
    "budget": fields.Float,
    "remaining": fields.Float,
    "start_date": fields.String,
    "end_date": fields.String,
    "created_on": fields.String,
    "progress": fields.Float,
    "length": fields.Integer
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
    "items": fields.List(fields.Nested(campaign_marshal)),
    "ad_requests": fields.List(fields.Nested({
        "id": fields.Integer,
        "campaign_id": fields.Integer,
        "influencer_id": fields.Integer,
        "status": fields.String,
        "created_on": fields.String
    }))
}

campaign_parser = reqparse.RequestParser()
campaign_parser.add_argument("sponsor_id", location="json")
campaign_parser.add_argument("name", location="json")
campaign_parser.add_argument("description", location="json")
campaign_parser.add_argument("goals", location="json")
campaign_parser.add_argument("category", location="json")
campaign_parser.add_argument("budget", location="json")
campaign_parser.add_argument("start_date", location="json")
campaign_parser.add_argument("end_date", location="json")
campaign_parser.add_argument("visibility", location="json")

search_parser = reqparse.RequestParser()
search_parser.add_argument("sponsor_id", help="Get all campaigns associated with Sponsor", location="json")
search_parser.add_argument("name", help="Search for campaigns with name like", location="json")
search_parser.add_argument("sort", help="Ascending or Descending", location="json")
search_parser.add_argument("category", help="Filter By Category", location="json")
search_parser.add_argument("page", help="Page Number", location="json")

class Campaigns(Resource):
    @auth_required('token')
    def get(self, campaign_id):
        campaign = get_campaign(campaign_id)
        campaign.length = get_campaign_ad_requests(campaign.id, 1).total
        if not campaign: return {"message": "Campaign Not Found"}, 400
        result = marshal(campaign, campaign_marshal)
        # Cache the result
        return result, 200
    
    @auth_required('token')    
    def put(self, campaign_id):
        args = campaign_parser.parse_args()
        valid, message = validate_update_campaign(campaign_id, args.get('name'), args.get('description'), args.get('start_date'), args.get('end_date'), 
                                                  args.get('category'), args.get('budget'), args.get('visibility'), args.get('goals'))
        if not valid: return {"message": message}, 400
        campaign = update_campaign(campaign_id, {"name": args.get('name'), "description": args.get('description'), "start_date": args.get('start_date'),
                                                 "end_date": args.get('end_date'), "category": args.get('category'), "budget": args.get('budget'),
                                                 "visibility": args.get('visibility'), "goals": args.get('goals')})
        return marshal(campaign, campaign_marshal), 200
    
    @auth_required('token')
    def delete(self, campaign_id):
        campaign = get_campaign(campaign_id)
        if not campaign: return {"message": "Campaign Not Found"}, 400
        ad_requests = get_campaign_ad_requests(campaign.id, -1)
        for ad_request in ad_requests:
            delete_ad_request(ad_request.id)
        delete_campaign(campaign_id)
        return {"message": "Campaign and associated Ad Requests Deleted Successfully"}, 200
    
    def post(self): return {"message": "POST not allowed"}, 405

class Create_Campaign(Resource):
    @auth_required('token')
    def post(self):
        args = campaign_parser.parse_args()
        if not args.get('sponsor_id'): return {"message": "Sponsor ID Missing"}, 400
        args['sponsor_id'] = int(args.get('sponsor_id'))
        sponsor = get_user('', id = args.get('sponsor_id'))
        if not sponsor: return {"message": "Sponsor Not Found"}, 400
        if "Sponsor" not in sponsor.roles: return {"message": "User is not a Sponsor"}, 400
        valid, message = validate_campaign(args.get('name'), args.get('description'), args.get('start_date'), args.get('end_date'), args.get('category'), 
                                           args.get('budget'), args.get('visibility'), args.get('goals'))
        if not valid: return {"message": message}, 400
        campaign = create_campaign(sponsor_id=args.get('sponsor_id'), name=args.get('name'), description=args.get('description'), start_date=args.get('start_date'),
                            end_date=args.get('end_date'), category=args.get('category'), budget=args.get('budget'), visibility=args.get('visibility'),
                            goals=args.get('goals'))
        return marshal(campaign, campaign_marshal), 201
    
    def get(self): return {"message": "GET not allowed"}, 405
    def put(self): return {"message": "PUT not allowed"}, 405
    def delete(self): return {"message": "DELETE not allowed"}, 405

class Search_Campaigns(Resource):
    @auth_required('token')
    def post(self):
        args = search_parser.parse_args()
        if args.get('sponsor_id'): 
            campaigns = get_sponsor_campaigns(args.get('sponsor_id'), int(args.get('page', -1)))
        else:
            campaigns = search_campaign(args.get('name'), args.get('sort'), args.get('category'), int(args.get('page', -1)))
        for campaign in campaigns.items:
            campaign.length = get_campaign_ad_requests(campaign.id, 1).total
        return marshal(campaigns, pagination_marshal), 200
    
    def get(self): return {"message": "GET not allowed"}, 405
    def put(self): return {"message": "PUT not allowed"}, 405
    def delete(self): return {"message": "DELETE not allowed"}, 405

class Sponsor_Campaigns(Resource):
    @auth_required('token')
    def post(self):
        args = search_parser.parse_args()
        campaigns = get_sponsor_campaigns(args.get('sponsor_id'), -1)
        for i in range(len(campaigns)):
            campaigns[i] = marshal(campaigns[i], campaign_marshal)
        return campaigns, 200
    
    def get(self): return {"message": "GET not allowed"}, 405
    def put(self): return {"message": "PUT not allowed"}, 405
    def delete(self): return {"message": "DELETE not allowed"}, 405

class All_Campaigns(Resource):
    @auth_required('token')
    def post(self):
        args = search_parser.parse_args()
        campaigns = get_all_campaigns(int(args.get('page', 1)))
        for campaign in campaigns.items:
            campaign.length = get_campaign_ad_requests(campaign.id, 1).total
        return marshal(campaigns, pagination_marshal), 200
    
    def get(self): return {"message": "GET not allowed"}, 405
    def put(self): return {"message": "PUT not allowed"}, 405
    def delete(self): return {"message": "DELETE not allowed"}, 405
            