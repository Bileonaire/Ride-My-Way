"""Handles data storage for Users, books and borrowed books
"""
# pylint: disable=E1101
import datetime

from flask import make_response, jsonify
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Contains user columns and methods to add, update and delete a user"""


    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    usertype = db.Column(db.String(250), nullable=False)
    carmodel = db.Column(db.String(250), nullable=True)
    numberplate = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return '<user {}>'.format(self.user)


    @classmethod
    def create_user(cls, username, email, password, usertype, carmodel=None, numberplate=None):
        """Creates a new user and ensures that the email is unique"""

        by_email = cls.query.filter_by(email=email).first()

        if by_email is None:
            password = generate_password_hash(password, method='sha256')
            new_user = cls(username=username, email=email, password=password, usertype=usertype,
                           carmodel=carmodel, numberplate=numberplate)
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify({
                "message" : "user has been successfully created",
                str(new_user.id) : {"username" : new_user.username,
                                    "email" : new_user.email, "password" : new_user.password,
                                    "usertype" : new_user.usertype,
                                    "carmodel" : new_user.carmodel,
                                    "numberplate" : new_user.numberplate}}), 201)
                                    


        return make_response(jsonify({"message" : "user with that email already exists"}), 400)


    @staticmethod
    def update_user(user_id, username, email, password, usertype, carmodel=None, numberplate=None):
        """Updates user information"""
        user = User.query.get(user_id)
        by_email = User.query.filter_by(email=email).first()

        if user is None:
            return make_response(jsonify({"message" : "user does not exists"}), 404)

        if by_email is None:
            user.username = username
            user.email = email
            user.password = generate_password_hash(password, method='sha256')
            user.usertype = usertype
            user.carmodel = carmodel
            user.numberplate = numberplate
            db.session.commit()

            return make_response(jsonify({
                "message" : "user has been successfully updated",
                str(user.id) : {"username" : user.username,
                                    "email" : user.email, "password" : user.password,
                                    "usertype" : user.usertype,
                                    "carmodel" : user.carmodel,
                                    "numberplate" : user.numberplate}}), 200)

        return make_response(jsonify({"message" : "user with that email already exists"}), 400)


    @staticmethod
    def delete_user(user_id):
        """Deletes a user"""
        user = User.query.filter_by(id=user_id).first()

        if user is None:
            return make_response(jsonify({"message" : "user does not exists"}), 404)

        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message" : "user has been successfully deleted"}), 200)


    @staticmethod
    def get_user(user_id):
        """Gets a particular user"""
        user = User.query.filter_by(id=user_id).first()
        all_rides = Ride.query.all()
        all_requests = Request.query.all()

        if user is None:
            return make_response(jsonify({"message" : "user does not exists"}), 404)
        
        if user.usertype == "driver":
            profile = {user.id : {"Username" : user.username, "Email" : user.email,
                                    "Usertype" : user.usertype,
                                    "Car Model" : user.carmodel,
                                    "Number Plate" : user.numberplate,
                                    "Rides already given" : [], "Rides pending" : []}}
            for ride in all_rides:
                if ride.driver_id == user.id:
                    trip = ride.departurepoint + " to " + ride.destination
                    if ride.status == "given":
                        profile[user.id]["Rides already given"].append(trip)
                    profile[user.id]["Rides pending"].append(trip)
        else:
            profile = {user.id : {'username' : user.username, 'email' : user.email,
                                    'usertype' : user.usertype,
                                    'Rides already taken' : [],
                                    'Rides pending' : [], 'Rides rejected' : []}}
            for request in all_requests:
                if request.user_id == user.id:
                    riderequest = Ride.query.filter_by(id=request.ride_id).first()
                    ride = riderequest.departurepoint + " to " + riderequest.destination
                    if request.status == "taken":
                        profile[user.id]["Rides already taken"].append(ride)
                    if request.status == "pending":
                        profile[user.id]["Rides pending"].append(ride)
                    if request.status == "rejected":
                        profile[user.id]["Rides rejected"].append(ride)

        return make_response(jsonify(profile), 200)
    
    @staticmethod
    def get_all_users():
        """Gets all users"""

        all_users = User.query.all()
        all_rides = Ride.query.all()
        all_requests = Request.query.all()

        users = []
        for user in all_users:

            if user.usertype == "driver":
                profile = {user.id : {"Username" : user.username, "Email" : user.email,
                                        "Usertype" : user.usertype,
                                        "Car Model" : user.carmodel,
                                        "Number Plate" : user.numberplate,
                                        "Rides already given" : [], "Rides pending" : []}}
                for ride in all_rides:
                    if ride.driver_id == user.id:
                        trip = ride.departurepoint + " to " + ride.destination
                        if ride.status == "given":
                            profile[user.id]["Rides already given"].append(trip)
                        profile[user.id]["Rides pending"].append(trip)
            else:
                profile = {user.id : {'username' : user.username, 'email' : user.email,
                                        'usertype' : user.usertype,
                                        'Rides already taken' : [],
                                        'Rides pending' : [], 'Rides rejected' : []}}
                for request in all_requests:
                    if request.user_id == user.id:
                        ride = Ride.query.filter_by(id=request.ride_id).first()
                        ride = ride.departurepoint + " to " + ride.destination
                        if request.status == "taken":
                            profile[user.id]["Rides already taken"].append(ride)
                        if request.status == "pending":
                            profile[user.id]["Rides pending"].append(ride)
                        if request.status == "rejected":
                            profile[user.id]["Rides rejected"].append(ride)

            users.append(profile)

        return {"all_users" : users}

class Ride(db.Model):
    """Contains ride columns and methods to add, update and delete a ride"""
    

    __tablename__ = 'ride'
    id = db.Column(db.Integer, primary_key=True)
    departurepoint = db.Column(db.String(250), nullable=False)
    destination = db.Column(db.String(250), nullable=False)
    departuretime = db.Column(db.String(250), nullable=False)
    cost = db.Column(db.String, nullable=False)
    maximum = db.Column(db.Integer, nullable=False)
    driver_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(250), nullable=False)


    def __repr__(self):
        return '<ride {}>'.format(self.ride)


    @classmethod
    def create_ride(cls, departurepoint, destination, driver_id,
                    departuretime, cost, maximum, status="pending"):
        """Creates a new ride"""

        new_ride = cls(departurepoint=departurepoint, destination=destination,
                       driver_id=driver_id, departuretime=departuretime,
                       cost=cost, maximum=maximum, status="pending")
        db.session.add(new_ride)
        db.session.commit()
        return make_response(jsonify({
            "message" : "ride has been successfully created",
            str(new_ride.id) : {"trip" : new_ride.departurepoint + " to " + new_ride.destination,
                                "driver_id": new_ride.driver_id,
                                "departuretime": new_ride.departuretime,
                                "cost": new_ride.cost, "maximum": new_ride.maximum,
                                "passengers" : [], "status" : new_ride.status}}), 201)

    @staticmethod
    def update_ride(ride_id, departurepoint, destination, driver_id, departuretime, cost,
                    maximum):
        """Updates ride information"""
        updateride = Ride.query.filter_by(id=ride_id).first()

        if updateride is None:
            return make_response(jsonify({"message" : "ride does not exists"}), 404)

        updateride.departurepoint = departurepoint
        updateride.destination = destination
        updateride.driver_id = driver_id
        updateride.departuretime = departuretime
        updateride.cost = cost
        updateride.maximum = maximum

        db.session.commit()
        passengers = []
        requests = Request.query.filter_by(ride_id=updateride.id, accepted=True).all()
        for request in requests:
            user = User.query.filter_by(user_id=request.user_id).first()
            passengers.append(user.username)

        return make_response(jsonify({
            "message" : "book has been successfully updated",
            str(updateride.id) : {"trip" : updateride.departurepoint + " to " + updateride.destination,
                                  "driver_id": updateride.driver_id,
                                  "departuretime": updateride.departuretime,
                                  "cost": updateride.cost, "maximum": updateride.maximum,
                                  "passengers" : passengers, "status" : updateride.status}}), 200)


    @staticmethod
    def start_ride(ride_id, driver_id):
        """starts a ride"""

        ride = Ride.query.filter_by(id=ride_id).first()
        if ride != None:

            if ride.driver_id == driver_id:
                ride.status = "given"

                requests = Request.query.filter_by(ride_id=ride.id).all()
                for request in requests:
                    if request.accepted is True:
                        request.status = "taken"
                    elif request.accepted is False:
                        request.status = "rejected"
                db.session.commit()

                return {"message" : "ride has started"}

            return {"message" : "The ride you want to start is not your ride."}
        return {"message" : "ride does not exist"}

    @staticmethod
    def delete_ride(ride_id):
        """Deletes a ride"""
        ride = Ride.query.filter_by(id=ride_id).first()

        if ride is None:
            return make_response(jsonify({"message" : "ride does not exists"}), 404)

        db.session.delete(ride)
        db.session.commit()
        return make_response(jsonify({"message" : "ride has been successfully deleted"}), 200)


    @staticmethod
    def get_ride(ride_id):
        """Gets a particular ride"""
        ride = Ride.query.get(ride_id)

        if ride != None:
            passengers = []
            requests = Request.query.filter_by(ride_id=ride.id, accepted=True).all()
            for request in requests:
                user = User.query.filter_by(id=request.user_id).first()
                passengers.append(user.username)

            info = {str(ride.id) : {"trip" : ride.departurepoint + " to " + ride.destination,
                                    "driver_id": ride.driver_id,
                                    "departuretime": ride.departuretime,
                                    "cost": ride.cost, "maximum": ride.maximum,
                                    "passengers" : passengers, "status" : ride.status}}

            return make_response(jsonify({ride.id : info}), 200)

        return make_response(jsonify({"message" : "ride does not exists"}), 404)
        
    
    @staticmethod
    def get_all_rides():
        """Gets all rides"""
        rides = Ride.query.all()
        get_all = []

        for ride in rides:
        
            passengers = []
            requests = Request.query.filter_by(ride_id=ride.id, accepted=True).all()
            for request in requests:
                user = User.query.filter_by(id=request.user_id).first()
                passengers.append(user.username)

                info = {str(ride.id) : {"trip" : ride.departurepoint + " to " + ride.destination,
                                        "driver_id": ride.driver_id,
                                        "departuretime": ride.departuretime,
                                        "cost": ride.cost, "maximum": ride.maximum,
                                        "passengers" : passengers, "status" : ride.status}}
            
                get_all.append(info)
            

        return make_response(jsonify({"All rides" : get_all}), 200)


class Request(db.Model):
    """Contains menu columns and methods to add, update and delete a request"""
   
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    ride_id = db.Column(db.Integer, nullable=False)
    driver_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    accepted = db.Column(db.Boolean)
    status = db.Column(db.String(250), nullable=False)

        
    def __repr__(self):
        return '<request {}>'.format(self.request)


    @classmethod
    def request_ride(cls, ride_id, user_id, accepted=False, status="pending"):
        """Creates a new request"""
        ride = Ride.query.filter_by(id=ride_id).first()
        if ride == None or ride.status == "given":
            return make_response(jsonify({"message" : "the ride is not available for request"}), 404)


        new_request = cls(ride_id=ride_id, user_id=user_id,
                            accepted=False, status="pending", driver_id=ride.driver_id)
        db.session.add(new_request)
        db.session.commit()

    
        return make_response(jsonify({"message" : "request has been successfully sent for approval",
                                    str(new_request.id) : {"ride_id" : new_request.ride_id,
                                                            "user_id": new_request.user_id,
                                                            "accepted": new_request.accepted,
                                                            "status" : new_request.status}}), 201)
            
        

    @staticmethod
    def delete_request(request_id):
        """Deletes a request"""

        try:
            request = Request.query.filter_by(id=request_id).first()
            db.session.delete(request)
            db.session.commit()
        except KeyError:
            return {"message" : "the specified request does not exist in requests"}
    
    @staticmethod
    def update_request(request_id):
        """Accepts/rejects request"""

        request = Request.query.get(request_id)
        ride = Ride.query.filter_by(id=request.ride_id).first()

        maximum = int(ride.maximum)
        passengers = []
        requests = Request.query.filter_by(ride_id=request.ride_id, accepted=True).all()
        for request in requests:
            user = User.query.filter_by(user_id=request.user_id).first()
            passengers.append(user.username)
        
        if len(passengers) < maximum:
            if request.accepted is False:
                request.accepted = True
                db.session.commit()
                return {"message" : "the request has been accepted"}

            elif request.accepted is True:
                request.accepted = False
                db.session.commit()
                return {"message" : "the request has been rejected"}
        else:
            if request.accepted is True:
                request.accepted = False
                db.session.commit()
                return {"message" : "the request has been rejected"}
            return {"message" : "the ride has reached its maximum number of passengers"}

    @staticmethod
    def get_requests(request_id):
        """Gets a particular request"""
        request = Request.query.filter_by(id=request_id).first()

        if request is None:
            return make_response(jsonify({"message" : "request does not exists"}), 404)
        
        user = User.query.filter_by(id=request.user_id).first()
        ride = Ride.query.filter_by(id=request.ride_id).first()

        info = {request.id : {"username" : user.username,
                "ride": ride.departurepoint + " to " + ride.destination,
                "driver_id" : ride.driver_id, "accepted": request.accepted,
                "status" : request.status}}

        return make_response(jsonify({"request" : info}), 200)


    @staticmethod
    def get_all_requests():
        """Gets all request"""
        requests = Request.query.all()

        if requests != None:
            request_list = []
            for request in requests:
                request = Request.query.filter_by(id=request.id).first()
                user = User.query.filter_by(id=request.user_id).first()
                ride = Ride.query.filter_by(id=request.ride_id).first()
                info = {request.id : {"username" : user.username,
                                      "ride": ride.departurepoint + " to " + ride.destination,
                                      "driver_id" : ride.driver_id, "accepted": request.accepted,
                                      "status" : request.status}}
                request_list.append(info)

            return make_response(jsonify({"all_requests" : request_list}), 200)
        return make_response(jsonify({"message" : "there are no requests"}), 404)
