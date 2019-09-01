# !/usr/bin/python
import os
import sys
import json
import inspect
import unittest
from unittest.mock import patch, Mock
import logging
import json
import jwt

currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from app import create_app
from models import db, ProviderModel
import requests
import re

# order_manager:
#   '/orders':
#     - 'GET'
#     - 'POST'
#     - 'PUT'
#     - 'DELETE'
# order_editor:
#   '/orders':
#     - 'GET'
#     - 'POST'
#     - 'PUT'
# order_inspector:
#   '/orders':
#     - 'GET'

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
        'name': 'provider_manager',
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
        


class ProviderTestCase(BaseTestCase):
    def test_new_provider(self):
        new_provider = {'name':'new_provider'}
        headers = {'Authorization': 'Bearer {0}'.format(self.jwtoken)}
        req = self.client().post('/providers', data=new_provider, headers=headers)
        self.assertEqual(req.status_code, 200)
        self.assertIn('_id', json.loads(req.data))
    
    # def test_get_providers(self):
    #     headers = {'Authorization': 'Bearer {0}'.format(self.jwtoken)}
    #     req = self.client().get('/providers',  headers=headers)
    #     self.assertEqual(req.status_code, 200)
    #     self.assertIn('_id', json.loads(req.data))

        
    def test_get_provider(self):
        new_provider = {'name':'new_provider1'}
        headers = {'Authorization': 'Bearer {0}'.format(self.jwtoken)}
        req = self.client().post('/providers', data=new_provider, headers=headers)
        get_res_json = json.loads(req.data)
        _id = get_res_json.get('_id')
        
        
        result = self.client().get('/providers/{0}'.format(_id), headers=headers)
        
        self.assertEqual(result.status_code, 200)
        provider = json.loads(result.data)
        self.assertEqual(provider['first_name'], new_provider['name'])

    def test_provider_can_be_edited(self):
        new_provider = {'name':'new_provider2'}
        headers = {'Authorization': 'Bearer {0}'.format(self.jwtoken)}
        req = self.client().post('/providers', data=new_provider, headers=headers)
        get_res_json = json.loads(req.data)
        _id = get_res_json.get('_id')
        rv = self.client().put(
            '/providers/{0}'.format(_id),
            data = {"name": "provider"}, headers=headers)
        self.assertEqual(rv.status_code, 200)
        result = self.client().get('/providers/{0}'.format(_id), headers=headers)
        provider = json.loads(result.data)
        self.assertEqual(provider['first_name'], "provider")

    def test_provider_deletion(self):
        provider = {'name': 'new_provider3'}
        headers = {'Authorization': 'Bearer {0}'.format(self.jwtoken)}
        req = self.client().post('/providers', data=provider, headers=headers)
        get_res_json = json.loads(req.data)
        _id = get_res_json.get('_id')
        
        res = self.client().delete('/providers/{0}'.format(_id), headers=headers)
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/providers/{0}'.format(_id), headers=headers)
        self.assertEqual(result.status_code, 404)



if __name__ == '__main__':
    unittest.main()
