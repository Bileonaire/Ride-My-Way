"""Test the ride endpoints on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import models
from .base_test import BaseTests


class RideTests(BaseTests):
    """Tests functionality of the ride endpoint"""


    def test_admin_get_one(self):
        """Tests admin successfully getting a ride"""
        response = self.app.get('/api/v2/rides/1', headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_user_get_one(self):
        """Tests user successfully getting a ride"""
        response = self.app.get('/api/v2/rides/2', headers=self.user_header)
        self.assertEqual(response.status_code, 200)
    
    def test_user_get_all(self):
        """Tests user successfully getting all ride"""
        response = self.app.get('/api/v2/rides',)
        self.assertEqual(response.status_code, 200)

    def test_get_non_existing(self):
        """Test getting a ride while providing non-existing id"""
        response = self.app.get('/api/v2/rides/300', headers=self.user_header)
        self.assertEqual(response.status_code, 404)

    def test_good_ride_update(self):
        """Test a successful ride update"""
        initial_data = json.dumps({"departurepoint" : "Syokimau", "destination" : "Nairobi",
         "departuretime" : "16/04/2015 1400HRS", "cost" : "400", "maximum" : "1"})
        added_ride = self.app.post( # pylint: disable=W0612
            '/api/v2/rides', data=initial_data,
            content_type='application/json',
            headers=self.driver_header)
        data = json.dumps({"departurepoint" : "Kayole", "destination" : "Nairobi",
         "departuretime" : "16/04/2015 1400HRS", "cost" : "400", "maximum" : "2"})
        response = self.app.put(
            '/api/v2/rides/2', data=data,
            content_type='application/json',
            headers=self.driver_header)
        self.assertEqual(response.status_code, 200)

    def test_bad_ride_create(self):
        """Test a unsuccessful ride create"""
        initial_data = json.dumps({"departurepoint" : "Syokimau", "destination" : "Nairobi",
         "departuretime" : "16/04/2015 1400HRS", "cost" : "400", "maximum" : "1"})
        added_ride = self.app.post( # pylint: disable=W0612
            '/api/v2/rides', data=initial_data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(added_ride.status_code, 401)
    
    def test_invalid_token_ride_create(self):
        """Test a unsuccessful ride create"""
        invalid_token = {
            "Content-Type" : "application/json",
            "x-access-token" : "hbGciOiJIUzI1NiJ9.eyJpZCI6NCwiYWRtaW4iOnRydWUsImV4cCI6MTUyNjczNzQ5Nvm2laNiJek7X266RLLk-bWL-ZF2RuD32FBvg_G8KyM"}
        initial_data = json.dumps({"departurepoint" : "Githuraiu", "destination" : "Nairobi",
         "departuretime" : "16/04/2015 1400HRS", "cost" : "400", "maximum" : "1"})
        added_ride = self.app.post( # pylint: disable=W0612
            '/api/v2/rides', data=initial_data,
            content_type='application/json',
            headers=invalid_token)
        self.assertEqual(added_ride.status_code, 401)

    def test_update_non_existing(self):
        """Test updating non_existing ride"""
        data = json.dumps({"departurepoint" : "Syokimau", "destination" : "Nairobi",
         "departuretime" : "16/04/2015 1400HRS", "cost" : "400", "maximum" : "1"})
        response = self.app.put(
            '/api/v2/rides/200', data=data,
            content_type='application/json',
            headers=self.driver_header)
        self.assertEqual(response.status_code, 404)

    def test_good_deletion(self):
        """Test a successful ride deletion"""
        response = self.app.delete('/api/v2/rides/1', headers=self.driver_header)
        self.assertEqual(response.status_code, 200)

    def test_no_header(self):
        """Test a unsuccessful ride deletion"""
        response = self.app.delete('/api/v2/rides/1',)
        self.assertEqual(response.status_code, 401)

    def test_deleting_non_existing(self):
        """Test deleting ride that does not exist"""
        response = self.app.delete('/api/v2/rides/200', headers=self.driver_header)
        self.assertEqual(response.status_code, 404)
    
    def test_start_ride(self):
        """Test starting a ride successfully"""
        response = self.app.post('/api/v2/rides/1', headers=self.driver_header)
        self.assertEqual(response.status_code, 200)
    
    def test_unsuccessful_start_ride(self):
        """Test starting a ride unsuccessfully"""
        response = self.app.post('/api/v2/rides/100', headers=self.driver_header2)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
