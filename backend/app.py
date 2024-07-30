from flask import Flask
from flask_security import Security
from flask_cors import CORS

from components.extensions import bcrypt, datastore
from components.models import db
from components.api import api
from components.authentication import authentication
from config import DevelopmentConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    bcrypt.init_app(app)
    api.init_app(app)
    app.security = Security(app, datastore)
    app.register_blueprint(authentication)
    
    # CORS for separate servers
    CORS(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run()