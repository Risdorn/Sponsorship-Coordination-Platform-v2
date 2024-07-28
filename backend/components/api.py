from flask_restful import Api

from .api_components.campaign import Campaigns, Create_Campaign, All_Campaigns
from .api_components.ad_request import Ad_requests, Create_Ad_Request, Revert_Ad_Request, Negotiate_Ad_Request, All_Ad_Requests
from .api_components.user import Users, Search_Influencer

api = Api(prefix="/api")

# Campaign End Points
api.add_resource(Campaigns, '/campaign/<int:campaign_id>')
api.add_resource(Create_Campaign, '/campaign')
api.add_resource(All_Campaigns, '/campaign/search')

# Ad Request End Points
api.add_resource(Ad_requests, '/ad_request/<int:ad_request_id>')
api.add_resource(Create_Ad_Request, '/ad_request')
api.add_resource(Revert_Ad_Request, '/ad_request/revert/<int:ad_request_id>')
api.add_resource(Negotiate_Ad_Request, '/ad_request/negotiate/<int:ad_request_id>')
api.add_resource(All_Ad_Requests, '/ad_requests')

# User End Points
api.add_resource(Users, '/user/<int:user_id>')
api.add_resource(Search_Influencer, '/user/search')