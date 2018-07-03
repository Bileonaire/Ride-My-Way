"""Test the signup endpoint on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class SignupTests(BaseTests):
    """Tests functionality of the signup endpoint"""


    def test_good_signup(self):
        """Tests successfully signing up"""
        data = json.dumps({
            "username" : "mark", "email" : "mark@gmail.com",
            "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.post('/api/v2/auth/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_same_email_signup(self):
        """Tests successfully signing up"""
        data = json.dumps({
            "username" : "user",
            "email" : "user@gmail.com",
            "password" : "12345678",
            "confirm_password" : "12345678"})
        response = self.app.post('/api/v2/auth/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_same_email_signup_driver(self):
        """Tests successfully signing up"""
        data = json.dumps({
            "username" : "driver1",
            "email" : "driver1@gmail.com",
            "password" : "123456789",
            "confirm_password" : "123456789"})
        response = self.app.post('/api/v2/auth/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_signup_diff_passwords(self):
        """Test unsuccessful signup because of unmatching passwords"""
        data = json.dumps({
            "username" : "felix", "email" : "felix@gmail.com",
            "password" : "12345678", "confirm_password" : "passwordsecret"})
        response = self.app.post('/api/v2/auth/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_signup_short_passwords(self):
        """Test unsuccessful signup because of short passwords"""
        data = json.dumps({
            "username" : "moses", "email" : "moses@gmail.com",
            "password" : "1234567", "confirm_password" : "1234567"})
        response = self.app.post('/api/v2/auth/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_signup_empty_username(self):
        """Test unsuccessful signup because of empty username"""
        data = json.dumps({
            "username" : "", "email" : "emptyusername@gmail.com",
            "password" : "12345678", "confirm_password" : "12345678"})
        response = self.app.post('/api/v2/auth/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_signup_invalid_email(self):
        """Test unsuccessful signup because of invalid email"""
        data = json.dumps({
            "username" : "lenny", "email" : "invalidemail.com",
            "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.post('/api/v2/auth/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_signup_empty_password(self):
        """Tests unsuccessful signup because of empty password"""
        data = json.dumps({
            "username" : "lenny", "email" : "lennymutush@gmail.com",
            "password" : "", "confirm_password" : "secret12345"})
        response = self.app.post('/api/v2/auth/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_signup_empty_conf_password(self):
        """Tests unsuccessful signup because of empty confirm_password"""
        data = json.dumps({
            "username" : "lenny", "email" : "confpassword@gmail.com",
            "password" : "secret", "confirm_password" : ""})
        response = self.app.post('/api/v2/auth/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
