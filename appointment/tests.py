# !/usr/bin/python
import os
import sys
import json
import inspect
import unittest
import logging
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from app import create_app
from models import db, RoleModel


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('config.TestingConfig')
        self.app = app
        self.client = self.app.test_client
        with self.app.app_context():
            db.create_all()
            

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            os.unlink(self.app.config.get('DATABASE'))


class AuthorizationTestCase(BaseTestCase):
    """ Tests correct user authentication """

    # ENDPOINT: POST '/acls'
    def test_acls(self):
        new_role = {'name':'new_role'}
        jwtoken = "token"
        headers = {'Authorization': 'Bearer {0}'.format(jwtoken)}
        req = self.client().post('/acls', data=new_role)
        self.assertEqual(req.status_code, 200)
        self.assertIn('_id', json.loads(req.data))
        
    def test_get_role(self):
        new_role = {'name':'new_role1'}
        jwtoken = "token"
        headers = {'Authorization': 'Bearer {0}'.format(jwtoken)}
        req = self.client().post('/acls', data=new_role, headers=headers)
        get_res_json = json.loads(req.data)
        _id = get_res_json.get('_id')
        
        
        result = self.client().get('/acl/{0}'.format(_id), headers=headers)
        
        self.assertEqual(result.status_code, 200)
        role = json.loads(result.data)
        self.assertEqual(role['name'], new_role['name'])

    def test_role_can_be_edited(self):
        new_role = {'name':'new_role2'}
        jwtoken = "token"
        headers = {'Authorization': 'Bearer {0}'.format(jwtoken)}
        req = self.client().post('/acls', data=new_role, headers=headers)
        get_res_json = json.loads(req.data)
        _id = get_res_json.get('_id')
        rv = self.client().put(
            '/acl/{0}'.format(_id),
            data = {"name": "user"}, headers=headers)
        self.assertEqual(rv.status_code, 200)
        result = self.client().get('/acl/{0}'.format(_id), headers=headers)
        role = json.loads(result.data)
        self.assertEqual(role['name'], "user")

    def test_role_deletion(self):
        role = {'name': 'new_role3'}
        jwtoken = "token"
        headers = {'Authorization': 'Bearer {0}'.format(jwtoken)}
        req = self.client().post('/acls', data=role, headers=headers)
        get_res_json = json.loads(req.data)
        _id = get_res_json.get('_id')
        
        res = self.client().delete('/acl/{0}'.format(_id), headers=headers)
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/acl/{0}'.format(_id), headers=headers)
        self.assertEqual(result.status_code, 404)



if __name__ == '__main__':
    unittest.main()
