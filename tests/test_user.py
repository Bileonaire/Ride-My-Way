"""Test the user endpoint on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests
import models


class UsersTest(BaseTests):
    """Tests functionality of the user endpoint"""


    def test_admin_get_user(self):
        """Test admin getting one user by providing the user_id"""
        response = self.app.get('/api/v3/users/2', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_user_get_user(self):
        """Test non-admin user getting one user by providing the user_id"""
        response = self.app.get('/api/v3/users/2')
        self.assertEqual(response.status_code, 401)

    def test_get_non_existing(self):
        """Test getting a user while providing non-existing id"""
        response = self.app.get('/api/v3/users/500', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)
    
    def test_good_update(self):
        """Test a successful user update"""
        data = json.dumps({
            "username" : "update",
            "email" : "update1@gmail.com",
            "password" : "123456789",
            "confirm_password" : "123456789",
            "admin" : False})
        response = self.app.put(
            '/api/v3/users/3', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 200)
    
    def test_existing_email_update(self):
        """Test a successful user update"""
        data = json.dumps({
            "username" : "update",
            "email" : "admin@gmail.com",
            "password" : "123456789",
            "confirm_password" : "123456789",
            "admin" : False})
        response = self.app.put(
            '/api/v3/users/3', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_update_short_password(self):
        """Test unsuccessful user update because of short password"""
        data = json.dumps({
            "username" : "user1", "email" : "user1@gmail.com",
            "password" : "topsecr", "confirm_password" : "topsecr", "admin" : False})
        response = self.app.put(
            '/api/v3/users/3', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_update_diff_passwords(self):
        """Test unsuccessful user update because of unmatching passwords"""
        data = json.dumps({
            "username" : "user1", "email" : "user1@gmail.com",
            "password" : "topsecret157", "confirm_password" : "topsecret1", "admin" : False})
        response = self.app.put(
            '/api/v3/users/3', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_updating_non_existing(self):
        """Test updating non_existing user"""
        data = json.dumps({
            "username" : "user1", "email" : "user1@gmail.com",
            "password" : "topsecret1", "confirm_password" : "topsecret1", "admin" : False})
        response = self.app.put(
            '/api/v3/users/55', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_good_deletion(self):
        """Test a successful user deletion"""
        response = self.app.delete('/api/v3/users/2', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_non_existing(self):
        """Test a deleting user that does not exist"""
        response = self.app.delete('/api/v3/users/1500', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
