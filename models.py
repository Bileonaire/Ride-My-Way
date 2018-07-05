"""Handles data storage for Users, rides and requests
"""
# pylint: disable=E1101
import datetime

from flask import make_response, jsonify, current_app
from werkzeug.security import generate_password_hash
import psycopg2
import config
from databasesetup import db


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
        db_cursor = db.con()
        db_cursor.execute(new_user)
        db.commit()


    @staticmethod              
    def update_user(user_id, username, email, password, admin):
        """Updates user information"""
        try:
            db_cursor = db.con()
            db_cursor.execute("UPDATE users SET username=%s, email=%s, password=%s, admin=%s WHERE user_id=%s",
                                (username, email, password, admin, user_id))
            db.commit()
            return make_response(jsonify({"message" : "user has been successfully updated"}), 200)
        except:
            return make_response(jsonify({"message" : "user does not exist"}), 404)

    @staticmethod
    def delete_user(user_id):
        """Deletes a user"""
        try:
            db_cursor = db.con()
            db_cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
            db.commit()
            return make_response(jsonify({"message" : "user has been successfully deleted"}), 200)
        except:
            return make_response(jsonify({"message" : "user does not exists"}), 404)

    @staticmethod
    def get_user(user_id):
        """Gets a particular user"""
        db_cursor = db.con()
        db_cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
        user = db_cursor.fetchall()

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
        db_cursor = db.con()
        db_cursor.execute("SELECT * FROM users")
        users = db_cursor.fetchall()

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
        db_cursor = db.con()
        db_cursor.execute(new_ride)
        db.commit()

    @classmethod
    def create_ride(cls, ride, driver_id, departuretime, numberplate, maximum, status="pending"):
        """Creates a new ride"""

        cls(ride, driver_id, departuretime, numberplate, maximum, status)
        return make_response(jsonify({"message" : "ride has been successfully created"}), 201)

    @staticmethod
    def update_ride(ride_id, ride, driver_id, departuretime, numberplate,
                    maximum):
        """Updates ride information"""
        try:
            db_cursor = db.con()
            db_cursor.execute("UPDATE rides SET ride=%s, driver_id=%s, departuretime=%s, numberplate=%s, maximum=%s WHERE ride_id=%s",
                                  (ride, driver_id, departuretime, numberplate, maximum, ride_id))
            db.commit()
            return make_response(jsonify({"message" : "user has been successfully updated"}), 200)
        except:
            return make_response(jsonify({"message" : "user does not exist"}), 404)


    @staticmethod
    def start_ride(ride_id, driver_id):
        """starts a ride"""
        db_cursor = db.con()
        db_cursor.execute("SELECT * FROM rides WHERE ride_id=%s", (ride_id,))
        ride = db_cursor.fetchall()
        if ride != []:
            ride = ride[0]
            if int(ride[2]) == driver_id:
                db_cursor.execute("UPDATE rides SET status=%s WHERE ride_id=%s", ("given", ride_id))
                db.commit()

                return {"message" : "ride has started"}

            return {"message" : "The ride you want to start is not your ride."}

        return {"message" : "ride does not exist"}

    @staticmethod
    def delete_ride(ride_id):
        """Deletes a ride"""
        db_cursor = db.con()
        db_cursor.execute("SELECT * FROM rides")
        rides = db_cursor.fetchall()

        for ride in rides:
            if ride[0] == ride_id:
                db_cursor.execute("DELETE FROM rides WHERE ride_id=%s", (ride_id,))
                db.commit()

                return make_response(jsonify({"message" : "ride has been successfully deleted"}), 200)
        return make_response(jsonify({"message" : "user does not exists"}), 404)

    @staticmethod
    def get_ride(ride_id):
        """Gets a particular ride"""
        db_cursor = db.con()
        db_cursor.execute("SELECT * FROM rides WHERE ride_id=%s", (ride_id,))
        ride = db_cursor.fetchall()

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
        db_cursor = db.con()
        db_cursor.execute("SELECT * FROM rides")
        rides = db_cursor.fetchall()
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
        db_cursor = db.con()
        db_cursor.execute(new_request)
        db.commit()

    @classmethod
    def request_ride(cls, ride_id, user_id, accepted=False, status="pending"):
        """Creates a new request"""
        cls(ride_id, user_id, accepted, status)
        return make_response(jsonify({"message" : "request has been successfully sent for approval"}), 201)

    @staticmethod
    def delete_request(request_id):
        """Deletes a request"""

        try:

            db_cursor = db.con()
            db_cursor.execute("DELETE FROM request WHERE request_id=%s", (request_id,))
            db.commit()

            return make_response(jsonify({"message" : "ride has been successfully deleted"}), 200)
        except:
            return make_response(jsonify({"message" : "the specified request does not exist in requests"}), 404)

    @staticmethod
    def accept_request(request_id):
        """Accepts request"""

        try:
            db_cursor = db.con()
            db_cursor.execute("UPDATE request SET accepted=%s WHERE request_id=%s", (True, request_id))
            db.commit()
            return make_response(jsonify({"message" : "request has been successfully accepted"}), 200)
        except KeyError:
            return make_response(jsonify({"message" : "the specified request does not exist in requests"}), 404)


    @staticmethod
    def get_requests(request_id):
        """Gets a particular request"""
        db_cursor = db.con()
        db_cursor.execute("SELECT * FROM request WHERE request_id=%s", (request_id,))
        request = db_cursor.fetchall()

        if request != []:
            return make_response(jsonify({"profile" : request}), 200)
        return make_response(jsonify({"message" : "request does not exists"}), 404)

    @staticmethod
    def get_particular_riderequests(ride_id):
        db_cursor = db.con()
        db_cursor.execute("SELECT * FROM request WHERE ride_id=%s", (ride_id,))
        requests = db_cursor.fetchall()

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
        db_cursor = db.con()
        db_cursor.execute("SELECT * FROM request")
        requests = db_cursor.fetchall()

        ride_requests = []
        for request in requests:
            info = {request[0] : {"user_id": request[1],
                                    "ride_id": request[2],
                                    "status": request[3],
                                    "accepted": request[4]}}
            ride_requests.append(info)
        return make_response(jsonify({"ride_requests" : ride_requests}), 200)

class Relation:
    """Contains method to get driver_id and maximum from a requested ride"""

    @staticmethod
    def get_driver_id(request_id):
        """Gets all request"""
        db_cursor = db.con()
        db_cursor.execute("SELECT * FROM request WHERE request_id=%s", (request_id,))
        request = db_cursor.fetchone()

        ride_id = str(request[2])
        print(ride_id)
        db_cursor = db.con()
        db_cursor.execute("SELECT * FROM request")
        rides = db_cursor.fetchall()
        print(rides)
        db_cursor = db.con()
        db_cursor.execute("SELECT driver_id FROM rides WHERE ride_id=%s", (ride_id,))
        driver_id = db_cursor.fetchone()
        print(driver_id)
        driver_id = driver_id[0]

        return str(driver_id)
    
    @staticmethod
    def get_maximum(request_id):
        """Gets all request"""
        db_cursor = db.con()
        db_cursor.execute("SELECT * FROM request WHERE request_id=%s", (str(request_id),))
        request = db_cursor.fetchone()

        db_cursor.execute("SELECT maximum FROM rides WHERE ride_id=%s", (request[2],))
        maximum = db_cursor.fetchone()
        maximum = maximum[0]

        return maximum
