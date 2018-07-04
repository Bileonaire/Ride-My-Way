"""Authenticate a user, driver and an admin to be used during testing
Set up required items to be used during testing
"""
# pylint: disable=W0612
import unittest
import json
from werkzeug.security import generate_password_hash
import psycopg2

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app
import models


class BaseTests(unittest.TestCase):
    """Authenticate a user and an admin and make the tokens available. Create a ride and request"""


    def setUp(self):
        self.application = app.create_app('config.TestingConfig')
        with self.application.app_context():
            models.tables_creation()

        user_reg = json.dumps({
            "username" : "user",
            "email" : "user@gmail.com",
            "password" : "12345678",
            "confirm_password" : "12345678"})

        driver_reg = json.dumps({
            "username" : "driver1",
            "email" : "driver1@gmail.com",
            "password" : "123456789",
            "confirm_password" : "123456789",
            "numberplate" : "KBA 375X",
            "carmodel" : "Subaru"})
        
        driver_reg2 = json.dumps({
            "username" : "driver2",
            "email" : "driver2@gmail.com",
            "password" : "123456789",
            "confirm_password" : "123456789",
            "numberplate" : "KBX 375X",
            "carmodel" : "Subaru"})

        self.user_log = json.dumps({
            "email" : "user@gmail.com",
            "password" : "12345678"})

        self.driver_log = json.dumps({
            "email" : "driver1@gmail.com",
            "password" : "123456789"})
        
        self.driver_log2 = json.dumps({
            "email" : "driver2@gmail.com",
            "password" : "123456789"})

        self.admin_log = json.dumps({
            "email" : "admin@gmail.com",
            "password" : "admin1234"})

        self.app = self.application.test_client()

        
        register_user = self.app.post(
            '/api/v3/auth/userregister', data=user_reg,
            content_type='application/json')
        register_driver = self.app.post(
            '/api/v3/auth/driverregister', data=driver_reg,
            content_type='application/json')
        
        register_driver2 = self.app.post(
            '/api/v3/auth/driverregister', data=driver_reg2,
            content_type='application/json')

        admin_result = self.app.post(
            '/api/v3/auth/login', data=self.admin_log,
            content_type='application/json')
        
        admin_response = json.loads(admin_result.get_data(as_text=True))
        admin_token = admin_response["token"]
        self.admin_header = {"Content-Type" : "application/json", "x-access-token" : admin_token}

        driver_result = self.app.post(
            '/api/v3/auth/login', data=self.driver_log,
            content_type='application/json')

        driver_response = json.loads(driver_result.get_data(as_text=True))
        driver_token = driver_response["token"]
        self.driver_header = {"Content-Type" : "application/json", "x-access-token" : driver_token}

        driver_result2 = self.app.post(
            '/api/v3/auth/login', data=self.driver_log2,
            content_type='application/json')

        driver_response2 = json.loads(driver_result2.get_data(as_text=True))
        driver_token2 = driver_response2["token"]
        self.driver_header2 = {"Content-Type" : "application/json", "x-access-token" : driver_token2}
        
        user_result = self.app.post(
            '/api/v3/auth/login', data=self.user_log,
            content_type='application/json')

        user_response = json.loads(user_result.get_data(as_text=True))
        user_token = user_response["token"]
        self.user_header = {"Content-Type" : "application/json", "x-access-token" : user_token}

        ride = json.dumps({"departurepoint" : "Syokimau", "destination" : "Nairobi",
         "departuretime" : "16/04/2015 1400HRS", "cost" : "400", "maximum" : "2"})

        ride2 = json.dumps({"departurepoint" : "Syokimau2", "destination" : "Nairobi2",
         "departuretime" : "16/04/2015 1400HRS", "cost" : "400", "maximum" : "2"})

        create_ride = self.app.post(
            '/api/v3/rides', data=ride, content_type='application/json',
            headers=self.driver_header)

        create_ride2 = self.app.post(
            '/api/v3/rides', data=ride2, content_type='application/json',
            headers=self.driver_header)

        requestride = self.app.post(
            '/api/v3/rides/1/requests',
            headers=self.user_header)
        
        requestride = self.app.post(
            '/api/v3/rides/2/requests',
            headers=self.user_header)


    def tearDown(self):
        with self.application.app_context():
            db_connection = psycopg2.connect(models.db)
            db_cursor = db_connection.cursor()
            db_cursor.execute('DROP TABLE "users", "rides","request";')
            db_connection.commit()
            db_connection.close()
