"""Test the login endpoint on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class LoginTests(BaseTests):
    """Tests functionality of the login endpoint"""


    def test_good_login(self):
        """Test a successful login"""
        response = self.app.post('/api/v3/auth/login', data=self.user_log, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_email(self):
        """Test unsuccessful login because email fails email regex"""
        data = json.dumps({"email" : "usergmail.com", "password" : "12345678"})
        response = self.app.post('/api/v3/auth/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_wrong_email(self):
        """Test unsuccessful login because of wrong email"""
        data = json.dumps({"email" : "usergood@gmail.com", "password" : "12345678"})
        response = self.app.post('/api/v3/auth/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_empty_password(self):
        """Test unsuccessful login because of empty password"""
        data = json.dumps({"email" : "user@gmail.com", "password" : ""})
        response = self.app.post('/api/v3/auth/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_wrong_password(self):
        """Test unsuccessful login because of wrong password"""
        data = json.dumps({"email" : "user@gmail.com", "password" : "secretpassword"})
        response = self.app.post('/api/v3/auth/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
