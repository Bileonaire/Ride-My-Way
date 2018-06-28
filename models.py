"""Handles data storage for Users, rides and requests
"""
# pylint: disable=E1101
import datetime

from flask import make_response, jsonify
from werkzeug.security import generate_password_hash
import psycopg2

def tables_creation():
    commands = ("""
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            email VARCHAR(150) NOT NULL UNIQUE,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(450) NOT NULL,
            usertype VARCHAR(100) NOT NULL,
            carmodel VARCHAR(200) NULL,
            numberplate VARCHAR(200) NULL)
        """,
        """ CREATE TABLE rides (
                       ride_id SERIAL PRIMARY KEY,
                       ride VARCHAR(155) NOT NULL,
                       driver_id VARCHAR(50) NOT NULL,
                       departuretime VARCHAR(100) NOT NULL,
                       cost VARCHAR(100) NOT NULL,
                       maximum VARCHAR(100) NOT NULL,
                       status VARCHAR(100) NOT NULL)
        """,
        """ CREATE TABLE request (
                       request_id SERIAL PRIMARY KEY,
                       user_id INTEGER NOT NULL,
                       ride_id INTEGER NOT NULL,
                       status VARCHAR(100) NOT NULL,
                       accepted BOOLEAN NOT NULL)
        """
        )
    conn = None
    try:
        conn = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


class User(object):
    """Contains user columns and methods to add, update and delete a user"""


    @staticmethod
    def create_user(username, email, password, usertype, carmodel="", numberplate=""):
        """Creates a new user and ensures that the email is unique"""
        db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM users")
        rows = db_cursor.fetchall()
        for row in rows:
            if row[1] == email:
                return make_response(jsonify({"message" : "user with that email already exists"}), 400)

        password = generate_password_hash(password, method='sha256')
        new_user = "INSERT INTO users (username, email, password, usertype, carmodel, numberplate) VALUES " \
                    "('" + username + "', '" + email + "', '" + password + "', '" + usertype + "', '" + carmodel + "','" + numberplate + "' )"
        db_cursor.execute(new_user)
        db_connection.commit()
        db_connection.close()
        return make_response(jsonify({"message" : "user has been successfully created"}), 201)
                                    

    @staticmethod
    def update_user(user_id, username, email, password, usertype, carmodel="", numberplate=""):
        """Updates user information"""
        db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM users")
        rows = db_cursor.fetchall()
        for row in rows:
            if row[1] == email:
                return make_response(jsonify({"message" : "user with that email already exists"}), 400)

        for row in rows:
            if row[0] == user_id:
                db_cursor.execute("UPDATE users SET username=%s, email=%s, password=%s, usertype=%s, carmodel=%s, numberplate=%s WHERE user_id=%s",
                                  (username, email, password, usertype, carmodel, numberplate, user_id))
                return make_response(jsonify({"message" : "user has been successfully updated"}), 200)

        return make_response(jsonify({"message" : "user does not exist"}), 404)


    @staticmethod
    def delete_user(user_id):
        """Deletes a user"""
        db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM users")
        rows = db_cursor.fetchall()
        if rows != []:
            for row in rows:
                if row[0] == user_id:
                    db_cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
                    db_connection.commit()
                    db_connection.close()
                    return make_response(jsonify({"message" : "user has been successfully deleted"}), 200)
        
        return make_response(jsonify({"message" : "user does not exists"}), 404)

    @staticmethod
    def get_user(user_id):
        """Gets a particular user"""
        db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
        user = db_cursor.fetchall()
        if user != []:
            return make_response(jsonify({"profile" : user}), 200)
        return make_response(jsonify({"message" : "user does not exists"}), 404)


    @staticmethod
    def get_all_users():
        """Gets all users"""
        db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM users")
        users = db_cursor.fetchall()
        return make_response(jsonify({"all users" : users}), 200)

class Ride(object):
    """Contains ride columns and methods to add, update and delete a ride"""



    @staticmethod
    def create_ride(ride, driver_id, departuretime, cost, maximum, status="pending"):
        """Creates a new ride"""
        db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
        db_cursor = db_connection.cursor()
        new_ride = "INSERT INTO rides (ride, driver_id, departuretime, cost, maximum, status) VALUES " \
                    "('" + ride + "', '" + driver_id + "', '" + departuretime + "', '" + cost + "','" + maximum + "','" + status + "' )"
        db_cursor.execute(new_ride)
        db_connection.commit()
        db_connection.close()
        return make_response(jsonify({"message" : "ride has been successfully created"}), 201)


    @staticmethod
    def update_ride(ride_id, ride, driver_id, departuretime, cost,
                    maximum):
        """Updates ride information"""
        db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM rides")
        rows = db_cursor.fetchall()
        for row in rows:
            if row[0] == ride_id:
                db_cursor.execute("UPDATE rides SET ride=%s, driver_id=%s, departuretime=%s, cost=%s, maximum=%s WHERE ride_id=%s",
                                  (ride, driver_id, departuretime, cost, maximum, ride_id))
                return make_response(jsonify({"message" : "ride has been successfully updated"}), 200)
        return make_response(jsonify({"message" : "ride does not exist"}), 404)


    @staticmethod
    def start_ride(ride_id, driver_id):
        """starts a ride"""
        db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM rides WHERE ride_id=%s", (ride_id,))
        rows = db_cursor.fetchall()
        if rows != []:
            row = rows[0]
            if int(row[2]) == driver_id:
                db_cursor.execute("UPDATE rides SET status=%s WHERE ride_id=%s",
                                ("given", ride_id))
                db_connection.commit()
                db_connection.close()
                return {"message" : "ride has started"}

            return {"message" : "The ride you want to start is not your ride."}

        return {"message" : "ride does not exist"}

    @staticmethod
    def delete_ride(ride_id):
        """Deletes a ride"""
        db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM rides")
        rows = db_cursor.fetchall()
        for row in rows:
            if row[0] == ride_id:
                db_cursor.execute("DELETE FROM rides WHERE ride_id=%s", (ride_id,))
                db_connection.commit()
                db_connection.close()
                return make_response(jsonify({"message" : "ride has been successfully deleted"}), 200)
        return make_response(jsonify({"message" : "user does not exists"}), 404)


    @staticmethod
    def get_ride(ride_id):
        """Gets a particular ride"""
        db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM rides WHERE ride_id=%s", (ride_id,))
        ride = db_cursor.fetchall()
        if ride != []:
            return make_response(jsonify({"profile" : ride}), 200)
        return make_response(jsonify({"message" : "ride does not exists"}), 404)
        
    
    @staticmethod
    def get_all_rides():
        """Gets all rides"""
        db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM rides")
        rides = db_cursor.fetchall()
        return make_response(jsonify({"all rides" : rides}), 200)

class Request(object):
    """Contains menu columns and methods to add, update and delete a request"""


    @staticmethod
    def request_ride(ride_id, user_id, accepted=False, status="pending"):
        """Creates a new request"""
        ride_id = str(ride_id)
        user_id = str(user_id)
        db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
        db_cursor = db_connection.cursor()
        new_request = "INSERT INTO request (ride_id, user_id, accepted, status) VALUES " \
                    "('" + ride_id + "', '" + user_id + "', '" + '0' + "', '" + status + "')"
        db_cursor.execute(new_request)
        db_connection.commit()
        db_connection.close()
        return make_response(jsonify({"message" : "request has been successfully sent for approval"}), 201)
            

    @staticmethod
    def delete_request(request_id):
        """Deletes a request"""

        try:
            db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
            db_cursor = db_connection.cursor()
            db_cursor.execute("DELETE FROM request WHERE request_id=%s", (request_id,))
            db_connection.commit()
            db_connection.close()
            return make_response(jsonify({"message" : "ride has been successfully deleted"}), 200)
        except:
            return make_response(jsonify({"message" : "the specified request does not exist in requests"}), 404)
    
    @staticmethod
    def update_request(request_id):
        """Accepts/rejects request"""
        try:
            db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
            db_cursor = db_connection.cursor()
            db_cursor.execute("UPDATE request SET status=%s WHERE request_id=%s",
                                  ("accepted", request_id))
            db_connection.commit()
            db_connection.close()
            return make_response(jsonify({"message" : "ride has been successfully deleted"}), 200)
        except KeyError:
            return make_response(jsonify({"message" : "the specified request does not exist in requests"}), 404)


    @staticmethod
    def get_requests(request_id):
        """Gets a particular request"""
        db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM request WHERE request_id=%s", (request_id,))
        request = db_cursor.fetchall()
        if request != []:
            return make_response(jsonify({"profile" : request}), 200)
        return make_response(jsonify({"message" : "ride does not exists"}), 404)


    @staticmethod
    def get_all_requests():
        """Gets all request"""
        db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM request")
        requests = db_cursor.fetchall()
        return make_response(jsonify({"all requests" : requests}), 200)
