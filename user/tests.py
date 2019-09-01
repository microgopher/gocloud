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
from models import db, UserModel

logging.basicConfig(level=logging.DEBUG)

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('config.TestingConfig')
        self.user = {'username':'test1', 'password': '1234'}
        self.app = app
        self.client = self.app.test_client
        with self.app.app_context():
            db.create_all()
            self.client().post('/auth/register', data=self.user)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            os.unlink(self.app.config.get('DATABASE'))


class AuthenticationTestCase(BaseTestCase):
    """ Tests correct user authentication """

    # ENDPOINT: POST '/auth/register'
    def test_registration(self):
        """Tests for correct user registration """
        new_user = {'username':'new_user' ,'password': 'test3'}
        req = self.client().get('/auth/register')
        self.assertEqual(req.status_code, 405)
        req = self.client().post('/auth/register', data=new_user)
        self.assertEqual(req.status_code, 200)
        
        self.assertIn('access_token', json.loads(req.data))
        # test for empty registration: respond with bad request
        rv = self.client().post('/auth/register')
        self.assertEqual(rv.status_code, 400)

    def test_user_already_exists(self):
        """Tests for the already existing user """
        user = {'username':'test1', 'password': 'Hello'}
        req = self.client().post('/auth/register', data=user)
        self.assertEqual(req.status_code, 201)
        self.assertNotIn('access_token', json.loads(req.data))
        

    # ENDPOINT: POST '/auth/login'
    def test_logging_in(self):
        """Tests correct user login """
        req = self.client().post('/auth/login', data=self.user)
        self.assertEqual(req.status_code, 200)
        self.assertIn('access_token', json.loads(req.data))
        
        rv = self.client().get('/auth/login')
        self.assertEqual(rv.status_code, 405)
        
        # test for invalid credentials: respond with unauthorized
        wrong_req = self.client().post(
            '/auth/login',
            data={'password': 'i have no idea', 'username':'test1'})
        self.assertEqual(wrong_req.status_code, 401)
        self.assertNotIn('access_token', json.loads(wrong_req.data))

    # ENDPOINT: GET '/auth/logout'
    def test_logging_out(self):
        """Test user correctly logging out"""
        get_res = self.client().post('/auth/login', data=self.user)
        get_res_json = json.loads(get_res.data)
        
        jwtoken = get_res_json.get('access_token')
        headers = {'Authorization': 'Bearer {0}'.format(jwtoken)}
        logout_req = self.client().post('/auth/logout', headers=headers)
        self.assertEqual(logout_req.status_code, 200)


    def test_get_logging_user(self):
        logger = logging.getLogger()
        get_res = self.client().post('/auth/login', data=self.user)
        get_res_json = json.loads(get_res.data)
        
        jwtoken = get_res_json.get('access_token')
        headers = {'Authorization': 'Bearer {0}'.format(jwtoken)}
        
        result = self.client().get('/users', headers=headers)
        
        self.assertEqual(result.status_code, 200)
        user = json.loads(result.data)
        self.assertEqual(user['username'], self.user['username'])

    def test_logging_user_can_be_edited(self):
        get_res = self.client().post('/auth/login', data=self.user)
        get_res_json = json.loads(get_res.data)
        
        jwtoken = get_res_json.get('access_token')
        headers = {'Authorization': 'Bearer {0}'.format(jwtoken)}
        rv = self.client().put(
            '/users',
            data={
                "name": "Happy",
                "mobile": "test"
            }, headers=headers)
        self.assertEqual(rv.status_code, 200)
        result = self.client().get('/users', headers=headers)
        user = json.loads(result.data)
        self.assertEqual(user['name'], "Happy")

    def test_logging_user_deletion(self):
        """Test API can delete an existing bucketlist. (DELETE request)."""
        inactive_user = {'username': 'inactive_user', 'password': 'inactive'}
        self.client().post('/auth/register', data=inactive_user)
        get_res = self.client().post('/auth/login', data=inactive_user)
        get_res_json = json.loads(get_res.data)
        
        jwtoken = get_res_json.get('access_token')
        headers = {'Authorization': 'Bearer {0}'.format(jwtoken)}
        
        res = self.client().delete('/users', headers=headers)
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/users', headers=headers)
        self.assertEqual(result.status_code, 404)



if __name__ == '__main__':
    unittest.main()
