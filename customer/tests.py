# !/usr/bin/python
import os
import sys
import json
import inspect
import unittest
from unittest.mock import patch, Mock
import jwt
import logging
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import requests
from app import create_app
from models import db, CustomerModel

class Auth:
    def __init__(self):
        self.auth_url = 'http://localhost:5000/auth/login'
    def login(self, username, password):
        response = requests.post(self.auth_url, {'username':username, 'password': password})
        return response.json()

def setup_auth_mock_patch():
    mock_auth_patcher = patch('tests.requests.post')
    roles = [{
        '_id': '99999999',
        'name': 'customer_manager',
        'permissions': ['get', 'post', 'put', 'delete']
    }]
    token_data = {
        'identity': '8888888888',
        'user_claims': {'username':'test1', 'userid':'8888888888','roles': roles}
    }
    access_token = jwt.encode(token_data, 'test123', 'HS256').decode('utf-8')
    mock_auth = mock_auth_patcher.start()
    mock_auth.return_value = Mock(status_code = 200)
    mock_auth.return_value.json.return_value = {'access_token': access_token}
    return mock_auth_patcher


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('config.TestingConfig')
        self.app = app
        self.client = self.app.test_client
        self.mock_auth_patcher = setup_auth_mock_patch()
        auth = Auth()
        res = auth.login('test1', '1234')
        self.jwtoken = res.get('access_token')
        with self.app.app_context():
            db.create_all()
            

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            os.unlink(self.app.config.get('DATABASE'))
            self.mock_auth_patcher.stop()


class CustomerTestCase(BaseTestCase):
    def test_new_customer(self):
        new_customer = {'name':'new_customer'}
        headers = {'Authorization': 'Bearer {0}'.format(self.jwtoken)}
        req = self.client().post('/customers', data=new_customer, headers=headers)
        self.assertEqual(req.status_code, 200)
        self.assertIn('_id', json.loads(req.data))
    
    # def test_get_customers(self):
    #     headers = {'Authorization': 'Bearer {0}'.format(self.jwtoken)}
    #     req = self.client().get('/customers',  headers=headers)
    #     self.assertEqual(req.status_code, 200)
    #     self.assertIn('_id', json.loads(req.data))

        
    def test_get_customer(self):
        new_customer = {'name':'new_customer1'}
        headers = {'Authorization': 'Bearer {0}'.format(self.jwtoken)}
        req = self.client().post('/customers', data=new_customer, headers=headers)
        get_res_json = json.loads(req.data)
        _id = get_res_json.get('_id')
        
        
        result = self.client().get('/customers/{0}'.format(_id), headers=headers)
        
        self.assertEqual(result.status_code, 200)
        customer = json.loads(result.data)
        self.assertEqual(customer['name'], new_customer['name'])

    def test_customer_can_be_edited(self):
        new_customer = {'name':'new_customer2'}
        headers = {'Authorization': 'Bearer {0}'.format(self.jwtoken)}
        req = self.client().post('/customers', data=new_customer, headers=headers)
        get_res_json = json.loads(req.data)
        _id = get_res_json.get('_id')
        rv = self.client().put(
            '/customers/{0}'.format(_id),
            data = {"name": "customer"}, headers=headers)
        self.assertEqual(rv.status_code, 200)
        result = self.client().get('/customers/{0}'.format(_id), headers=headers)
        customer = json.loads(result.data)
        self.assertEqual(customer['name'], "customer")

    def test_customer_deletion(self):
        customer = {'name': 'new_customer3'}
        headers = {'Authorization': 'Bearer {0}'.format(self.jwtoken)}
        req = self.client().post('/customers', data=customer, headers=headers)
        get_res_json = json.loads(req.data)
        _id = get_res_json.get('_id')
        
        res = self.client().delete('/customers/{0}'.format(_id), headers=headers)
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/customers/{0}'.format(_id), headers=headers)
        self.assertEqual(result.status_code, 404)

if __name__ == '__main__':
    unittest.main()
