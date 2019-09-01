from functools import wraps
from flask_restful import Resource, reqparse
from models import RoleModel
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_claims
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

class Roles(Resource):
    @auth_required
    def post(self):
        #TODO: permission and acticity details
        parser = reqparse.RequestParser()
        parser.add_argument('name', required = True)
        data = parser.parse_args()
        new_role = RoleModel(
            name = data['name'],
        )
        new_role.save()
        return {'_id': new_role.hex_id}, 200
        
class Role(Resource):
    @auth_required
    def put(self, _id):
        parser = reqparse.RequestParser()
        role = RoleModel.query.filter_by(hex_id=_id).first()
        if not role:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        parser.add_argument('name')
        
        data = parser.parse_args()
        role.name = data['name']
        role.save()
        return {}, 200

    @auth_required
    def delete(self, _id):
        role = RoleModel.query.filter_by(hex_id=_id).first()
        if not role:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        role.delete()
        return {}, 200

    @auth_required
    def get(self, _id):
        role = RoleModel.query.filter_by(hex_id=_id).first()
        
        if not role:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        response = jsonify({
            '_id': role.hex_id,
            'name': role.name,
            'date_created': role.date_created,
            'date_modified': role.date_modified
        })
        response.status_code = 200
        return response
            

        
        


