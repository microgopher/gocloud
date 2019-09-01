from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import jsonify
from flask_migrate import Migrate

import models, resources
from models import db

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

    # api resources go here
    api.add_resource(resources.Customers, '/customers', methods=['GET', 'POST'])
    api.add_resource(resources.Customer, '/customers/<string:_id>', methods=['GET', 'PUT', 'DELETE'])
    return app
