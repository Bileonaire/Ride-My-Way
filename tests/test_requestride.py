"""Test the ride request endpoints on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import models
from .base_test import BaseTests


class RequestRideTests(BaseTests):
    """Tests functionality of the request endpoint"""

    def test_user_request_ride(self):
        """Tests user successfully requesting a ride"""
        request_ride = self.app.post( # pylint: disable=W0612
            '/api/v2/rides/1/requests',
            headers=self.user_header)
        response = request_ride
        self.assertEqual(response.status_code, 201)
    
    def test_no_token_request_ride(self):
        """Tests user successfully requesting a ride"""
        request_ride = self.app.post( # pylint: disable=W0612
            '/api/v2/rides/1/requests')
        response = request_ride
        self.assertEqual(response.status_code, 401)

    def test_admin_get_allrequests(self):
        """Tests admin successfully getting all requests"""
        response = self.app.get('/api/v2/requests', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_user_get_one(self):
        """Tests user successfully getting a request"""
        response = self.app.get('/api/v2/requests/2', headers=self.user_header)
        self.assertEqual(response.status_code, 200)
    
    def test__get_ride_requests(self):
        """Tests user successfully getting a ride request"""
        response = self.app.get('/api/v2/rides/1/requests', headers=self.driver_header)
        self.assertEqual(response.status_code, 200)

    def test_unsuccessful_get_ride_requests(self):
        """Tests user successfully getting a ride request"""
        response = self.app.get('/api/v2/rides/500/requests', headers=self.driver_header)
        self.assertEqual(response.status_code, 404)

    def test_get_non_existing(self):
        """Test getting a request while providing non-existing id"""
        response = self.app.get('/api/v2/requests/50', headers=self.user_header)
        self.assertEqual(response.status_code, 404)

    def test_good_request_accept_reject(self):
        """Test a successful request update"""
        response = self.app.put(
            '/api/v2/requests/2',
            content_type='application/json',
            headers=self.driver_header)
        self.assertEqual(response.status_code, 200)

    # def test_bad_request_accept_reject(self):
    #     """Test an unsuccessful request update from a driver who does not own the trip"""
    #     response = self.app.put(
    #         '/api/v2/requests/2',
    #         content_type='application/json',
    #         headers=self.driver_header2)
    #     self.assertEqual(response.status_code, 404)

    def test_update_non_existing(self):
        response = self.app.put(
            '/api/v2/requests/50',
            content_type='application/json',
            headers=self.driver_header)
        self.assertEqual(response.status_code, 404)

    def test_good_deletion(self):
        """Test a successful request deletion"""
        response = self.app.delete('/api/v2/requests/1', headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_deleting_non_existing(self):
        """Test deleting request that does not exist"""
        response = self.app.delete('/api/v2/requests/500', headers=self.user_header)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
