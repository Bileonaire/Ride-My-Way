"""Handles data storage for Users, rides and requests
"""
# pylint: disable=E1101
import datetime

from flask import make_response, jsonify, current_app
from werkzeug.security import generate_password_hash
import psycopg2
import config

db = config.TestingConfig.db

def conn():
    """database connection"""

    db_conn = psycopg2.connect(db)
    return db_conn

class User():
    """Contains user columns and methods to add, update and delete a user"""


    def __init__(self, username, email, password, admin):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        if admin == True:
            self.admin = '1'
        else:
            self.admin = '0'

        new_user = "INSERT INTO users (username, email, password, admin) VALUES " \
                    "('" + self.username + "', '" + self.email + "', '" + self.password + "', '" + self.admin + "')"
        db_connection = conn()
        db_cursor = db_connection.cursor()
        db_cursor.execute(new_user)
        db_connection.commit()

                                    
    @staticmethod
    def update_user(user_id, username, email, password, admin):
        """Updates user information"""
        db_connection = conn()
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM users")
        users = db_cursor.fetchall()
        for user in users:
            if user[1] == email:
                return make_response(jsonify({"message" : "user with that email already exists"}), 400)

        for user in users:
            if user[0] == user_id:
                db_cursor.execute("UPDATE users SET username=%s, email=%s, password=%s, admin=%s WHERE user_id=%s",
                                  (username, email, password, admin, user_id))
                db_connection.commit()
                db_connection.close()

                return make_response(jsonify({"message" : "user has been successfully updated"}), 200)

        return make_response(jsonify({"message" : "user does not exist"}), 404)

    @staticmethod
    def delete_user(user_id):
        """Deletes a user"""
        db_connection = conn()
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM users")
        users = db_cursor.fetchall()
        if users != []:
            for user in users:
                if user[0] == user_id:
                    db_cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
                    db_connection.commit()
                    db_connection.close()

                    return make_response(jsonify({"message" : "user has been successfully deleted"}), 200)
        
        return make_response(jsonify({"message" : "user does not exists"}), 404)

    @staticmethod
    def get_user(user_id):
        """Gets a particular user"""
        db_connection = conn()
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
        user = db_cursor.fetchall()
        db_connection.close()

        if user != []:
            user=user[0]
            info = {user[0] : {"email": user[1],
                                "username": user[2],
                                "admin": user[4]}}
            return make_response(jsonify({"profile" : info}), 200)
        return make_response(jsonify({"message" : "user does not exists"}), 404)

    @staticmethod
    def get_all_users():
        """Gets all users"""
        db_connection = conn()
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM users")
        users = db_cursor.fetchall()
        db_connection.close()

        all_users = []
        for user in users:
            info = {user[0] : {"email": user[1],
                                "username": user[2],
                                "admin": user[4]}}
            all_users.append(info)
        return make_response(jsonify({"All users" : all_users}), 200)


class Ride():
    """Contains ride columns and methods to add, update and delete a ride"""


    def __init__(self, ride, driver_id, departuretime, numberplate, maximum, status):
        self.ride = ride
        self.driver_id = driver_id
        self.departuretime = departuretime
        self.numberplate = numberplate
        self.maximum = maximum
        self.status = status
        new_ride = "INSERT INTO rides (ride, driver_id, departuretime, numberplate, maximum, status) VALUES " \
                    "('" + self.ride + "', '" + self.driver_id + "', '" + self.departuretime + "', '" + self.numberplate + "','" + self.maximum + "','" + self.status + "' )"
        db_connection = conn()
        db_cursor = db_connection.cursor()
        db_cursor.execute(new_ride)
        db_connection.commit()

    @classmethod
    def create_ride(cls, ride, driver_id, departuretime, numberplate, maximum, status="pending"):
        """Creates a new ride"""

        cls(ride, driver_id, departuretime, numberplate, maximum, status)
        return make_response(jsonify({"message" : "ride has been successfully created"}), 201)

    @staticmethod
    def update_ride(ride_id, ride, driver_id, departuretime, numberplate,
                    maximum):
        """Updates ride information"""
        db_connection = conn()
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM rides")
        rides = db_cursor.fetchall()
        for ride in rides:
            if ride[0] == ride_id:
                db_cursor.execute("UPDATE rides SET ride=%s, driver_id=%s, departuretime=%s, numberplate=%s, maximum=%s WHERE ride_id=%s",
                                  (ride, driver_id, departuretime, numberplate, maximum, ride_id))
                db_connection.commit()
                db_connection.close()

                return make_response(jsonify({"message" : "ride has been successfully updated"}), 200)
        return make_response(jsonify({"message" : "ride does not exist"}), 404)

    @staticmethod
    def start_ride(ride_id, driver_id):
        """starts a ride"""
        db_connection = conn()
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM rides WHERE ride_id=%s", (ride_id,))
        ride = db_cursor.fetchall()
        if ride != []:
            ride = ride[0]
            if int(ride[2]) == driver_id:
                db_cursor.execute("UPDATE rides SET status=%s WHERE ride_id=%s", ("given", ride_id))
                db_connection.commit()
                db_connection.close()

                return {"message" : "ride has started"}

            return {"message" : "The ride you want to start is not your ride."}

        return {"message" : "ride does not exist"}

    @staticmethod
    def delete_ride(ride_id):
        """Deletes a ride"""
        db_connection = conn()
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM rides")
        rides = db_cursor.fetchall()

        for ride in rides:
            if ride[0] == ride_id:
                db_cursor.execute("DELETE FROM rides WHERE ride_id=%s", (ride_id,))
                db_connection.commit()
                db_connection.close()

                return make_response(jsonify({"message" : "ride has been successfully deleted"}), 200)
        return make_response(jsonify({"message" : "user does not exists"}), 404)

    @staticmethod
    def get_ride(ride_id):
        """Gets a particular ride"""
        db_connection = conn()
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM rides WHERE ride_id=%s", (ride_id,))
        ride = db_cursor.fetchall()
        db_connection.close()

        if ride != []:
            ride=ride[0]
            info = {ride[0] : {"ride": ride[1],
                                "driver_id": ride[2],
                                "departure_time": ride[3],
                                "cost": ride[4],
                                "maximum": ride[5],
                                "status": ride[6]}}
            return make_response(jsonify({"ride" : info}), 200)
        return make_response(jsonify({"message" : "ride does not exists"}), 404)
        
    @staticmethod
    def get_all_rides():
        """Gets all rides"""
        db_connection = conn()
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM rides")
        rides = db_cursor.fetchall()
        db_connection.close()
        all_rides = []
        for ride in rides:
            info = {ride[0] : {"ride": ride[1],
                                "driver_id": ride[2],
                                "departure_time": ride[3],
                                "cost": ride[4],
                                "maximum": ride[5],
                                "status": ride[6]}}
            all_rides.append(info)
        return make_response(jsonify({"All rides" : all_rides}), 200)


class Request:
    """Contains menu columns and methods to add, update and delete a request"""


    def __init__(self, ride_id, user_id, accepted, status):
        self.ride_id = str(ride_id)
        self.user_id = str(user_id)
        self.accepted = accepted
        self.status = status
        new_request = "INSERT INTO request (ride_id, user_id, accepted, status) VALUES " \
                    "('" + self.ride_id + "', '" + self.user_id + "', '" + '0' + "', '" + self.status + "')"
        db_connection = conn()
        db_connection = conn()
        db_cursor = db_connection.cursor()
        db_cursor.execute(new_request)
        db_connection.commit()

    @classmethod
    def request_ride(cls, ride_id, user_id, accepted=False, status="pending"):
        """Creates a new request"""
        cls(ride_id, user_id, accepted, status)
        return make_response(jsonify({"message" : "request has been successfully sent for approval"}), 201)

    @staticmethod
    def delete_request(request_id):
        """Deletes a request"""

        try:
            db_connection = conn()
            db_cursor = db_connection.cursor()
            db_cursor.execute("DELETE FROM request WHERE request_id=%s", (request_id,))
            db_connection.commit()
            db_connection.close()

            return make_response(jsonify({"message" : "ride has been successfully deleted"}), 200)
        except:
            return make_response(jsonify({"message" : "the specified request does not exist in requests"}), 404)

    @staticmethod
    def update_request(request_id):
        """Accepts request"""

        try:
            db_connection = conn()
            db_cursor = db_connection.cursor()
            db_cursor.execute("UPDATE request SET accepted=%s WHERE request_id=%s", (True, request_id))
            db_connection.commit()
            db_connection.close()

            return make_response(jsonify({"message" : "request has been successfully accepted"}), 200)
        except KeyError:
            return make_response(jsonify({"message" : "the specified request does not exist in requests"}), 404)
    
    @staticmethod
    def reject_request(request_id):
        """rejects request"""
        try:
            db_connection = conn()
            db_cursor = db_connection.cursor()
            db_cursor.execute("UPDATE request SET accepted=%s WHERE request_id=%s", (False, request_id))
            db_connection.commit()
            db_connection.close()

            return make_response(jsonify({"message" : "request has been successfully rejected"}), 200)
        except KeyError:
            return make_response(jsonify({"message" : "the specified request does not exist in requests"}), 404)

    @staticmethod
    def get_requests(request_id):
        """Gets a particular request"""
        db_connection = conn()
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM request WHERE request_id=%s", (request_id,))
        request = db_cursor.fetchall()
        db_connection.close()

        if request != []:
            return make_response(jsonify({"profile" : request}), 200)
        return make_response(jsonify({"message" : "ride does not exists"}), 404)

    @staticmethod
    def get_particular_riderequests(ride_id):
        db_connection = conn()
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM request WHERE ride_id=%s", (ride_id,))
        requests = db_cursor.fetchall()
        db_connection.close()

        if requests != []:
            ride_requests = []
            for request in requests:
                info = {request[0] : {"user_id": request[1],
                                        "ride_id": request[2],
                                        "status": request[3],
                                        "accepted": request[4]}}
                ride_requests.append(info)
            return make_response(jsonify({"ride_requests" : ride_requests}), 200)
        return make_response(jsonify({"message" : "ride does not exists"}), 404)

    @staticmethod
    def get_all_requests():
        """Gets all request"""
        db_connection = conn()
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM request")
        requests = db_cursor.fetchall()
        db_connection.close()

        ride_requests = []
        for request in requests:
            info = {request[0] : {"user_id": request[1],
                                    "ride_id": request[2],
                                    "status": request[3],
                                    "accepted": request[4]}}
            ride_requests.append(info)
        return make_response(jsonify({"ride_requests" : ride_requests}), 200)
