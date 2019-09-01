from functools import wraps
from flask_restful import Resource, reqparse
from models import CustomerModel
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_claims, get_jwt_identity
from flask import jsonify, abort

import app

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        valid = False
        if 'roles' in claims:
            for role in claims['roles']:
                permissions = role.get('permissions', [])
                if role['name'] == 'root' or fn.__name__ in permissions:
                    valid = True
                    break
        
        if not valid:
            return {'message': 'Invalid token!'}, 403
        return fn(*args, **kwargs)
    return wrapper

class Customers(Resource):
    @auth_required
    def post(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('name', required = True)
        data = parser.parse_args()
        current_user_id = get_jwt_identity()
        new_customer = CustomerModel(
            name = data['name'],
            user_id = current_user_id
        )
        new_customer.save()
        return {'_id': new_customer.hex_id}, 200
        
class Customer(Resource):
    @auth_required
    def put(self, _id):
        parser = reqparse.RequestParser()
        current_user_id = get_jwt_identity()
        customer = CustomerModel.query.filter_by(hex_id=_id, user_id=current_user_id).first()
        if not customer:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        parser.add_argument('name')
        
        data = parser.parse_args()
        customer.name = data['name']
        customer.save()
        return {}, 200

    @auth_required
    def delete(self, _id):
        current_user_id = get_jwt_identity()
        customer = CustomerModel.query.filter_by(hex_id=_id, user_id=current_user_id).first()
        if not customer:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        customer.delete()
        return {}, 200

    @auth_required
    def get(self, _id):
        current_user_id = get_jwt_identity()
        customer = CustomerModel.query.filter_by(hex_id=_id, user_id=current_user_id).first()
        
        if not customer:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        response = jsonify({
            '_id': customer.hex_id,
            'name': customer.name,
            'date_created': customer.date_created,
            'date_modified': customer.date_modified
        })
        response.status_code = 200
        return response