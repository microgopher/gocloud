from functools import wraps

from flask_restful import Resource, reqparse
from models import UserModel, RevokedTokenModel
from flask_jwt_extended import (create_access_token, get_jwt_claims, verify_jwt_in_request, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import jsonify, abort

import app

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        return fn(*args, **kwargs)
        # if claims['roles'] != 'admin':
        #     return jsonify(msg='Admins only!'), 403
        # else:
        #     return fn(*args, **kwargs)
    return wrapper

class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help = 'This field cannot be blank', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', required = True)
        parser.add_argument('mobile')
        parser.add_argument('email')
        parser.add_argument('name')


        data = parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}, 201
        
        new_user = UserModel(
            username = data['username'],
            mobile = data['mobile'],
            email = data['email'],
            name = data['name'],
            password = UserModel.generate_hash(data['password'])
        )
        
        
        new_user.save()
        claim = app.UserClaim(username=new_user.username, userid=new_user.hex_id, roles=new_user.roles)
        
        access_token = create_access_token(identity = claim)
        refresh_token = create_refresh_token(identity = claim)
        return {
            'message': 'User {} was created'.format(data['username']),
            'access_token': access_token,
            'refresh_token': refresh_token
        }
            
        

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help = 'This field cannot be blank', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', required = True)
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}, 406
        
        if UserModel.verify_hash(data['password'], current_user.password):
            claim = app.UserClaim(username=current_user.username, userid=current_user.hex_id, roles=current_user.roles)
            access_token = create_access_token(identity = claim)
            refresh_token = create_refresh_token(identity = claim)
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}, 401


class UserLogoutAccess(Resource):
    @auth_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.save()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class Users(Resource):
    @auth_required
    def put(self):
        parser = reqparse.RequestParser()
        current_user_id = get_jwt_identity()
        #current_roles = get_jwt_claims()
        
        user = UserModel.query.filter_by(hex_id=current_user_id, active=True).first()
        
        if not user:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        parser.add_argument('mobile')
        parser.add_argument('email')
        parser.add_argument('name')
        data = parser.parse_args()
        user.mobile = data['mobile']
        user.email = data['email']
        user.name = data['name']
        user.save()
        response = jsonify({
            '_id': user.hex_id,
            'username': user.username,
            'name': user.name,
            'mobile': user.mobile,
            'email': user.email,
            'date_created': user.date_created,
            'date_modified': user.date_modified
        })
        response.status_code = 200
        return response

    @auth_required
    def delete(self):
        current_user_id = get_jwt_identity()
        user = UserModel.query.filter_by(hex_id=current_user_id, active=True).first()
        if not user:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        user.active = False 
        user.save()
        return {
            "message": "user {} deleted successfully".format(user.username) 
         }, 200

    @auth_required
    def get(self):
        current_user_id = get_jwt_identity()
        
        user = UserModel.query.filter_by(hex_id=current_user_id, active=True).first()
        
        if not user:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        response = jsonify({
            '_id': user.hex_id,
            'username': user.username,
            'name': user.name,
            'mobile': user.mobile,
            'email': user.email,
            'date_created': user.date_created,
            'date_modified': user.date_modified
        })
        response.status_code = 200
        return response
            

        
        


