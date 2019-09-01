from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import jsonify

import models, resources
from models import db

class UserClaim:
    def __init__(self, username, userid, roles):
        self.userid = userid
        self.username = username
        self.roles = roles

def create_app(module='config.DevelopmentConfig'):
    """Wrap the routes into one exportable method """
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    # Object-based configuration
    app.config.from_object(module)
    # Initializes the app Api with set configs
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return models.RevokedTokenModel.is_jti_blacklisted(jti)

    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        return {'roles': user.roles, 'userid': user.userid, 'username': user.username}

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.userid

    # api resources go here
    api.add_resource(resources.UserRegistration, '/auth/register')
    api.add_resource(resources.UserLogin, '/auth/login')
    api.add_resource(resources.UserLogoutAccess, '/auth/logout')
    #api.add_resource(resources.UserLogoutRefresh, '/auth/logout/refresh')
    #api.add_resource(resources.TokenRefresh, '/auth/token/refresh')
    api.add_resource(resources.Users, '/users')
    return app

app = create_app()  