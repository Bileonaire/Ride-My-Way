"""Contains all endpoints to manipulate ride information
"""
import datetime

from flask import request, jsonify, Blueprint, make_response
from flask_restful import Resource, Api, reqparse, inputs
import jwt

import models
import config
from .auth import user_required, admin_required, driver_required, driver_admin_required


class RideList(Resource):
    """Contains GET and POST methods"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'departurepoint',
            required=True,
            type=str,
            help='kindly provide a departure point',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'destination',
            required=True,
            type=str,
            help="kindly provide a valid destination",
            location=['form', 'json'])
        self.reqparse.add_argument(
            'departuretime',
            required=True,
            location=['form', 'json'])
        self.reqparse.add_argument(
            'cost',
            required=True,
            location=['form', 'json'])
        self.reqparse.add_argument(
            'maximum',
            required=True,
            type=int,
            help="kindly provide a valid integer of the maximum number of passengers",
            location=['form', 'json'])
        super().__init__()
    
    @driver_required
    def post(self):
        """Adds a new ride"""
        kwargs = self.reqparse.parse_args()

        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        driver_id = data['id']

        result = models.Ride.create_ride(driverid=driver_id, **kwargs)
        return make_response(jsonify(result), 201)

    def get(self):
        """Gets all rides"""
        return make_response(jsonify(models.all_rides), 200)


class Ride(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single ride"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'departurepoint',
            required=True,
            type=str,
            help='kindly provide a departure point',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'destination',
            required=True,
            type=str,
            help="kindly provide a valid destination",
            location=['form', 'json'])
        self.reqparse.add_argument(
            'departuretime',
            required=True,
            location=['form', 'json'])
        self.reqparse.add_argument(
            'cost',
            required=True,
            location=['form', 'json'])
        self.reqparse.add_argument(
            'maximum',
            required=True,
            location=['form', 'json'])
        super().__init__()
    

    def get(self, ride_id):
        """Get a particular ride"""
        try:
            ride = models.all_rides[ride_id]
            return make_response(jsonify(ride), 200)
        except KeyError:
            return make_response(jsonify({"message" : "ride does not exist"}), 404)

    @driver_required
    def post(self, ride_id):
        """start a particular ride"""
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        driver_id = data['id']

        result = models.Ride.start_ride(ride_id, driver_id=driver_id)
        if result == {"message" : "ride has started"}:
            return make_response(jsonify(result), 200)
        return make_response(jsonify(result), 404)
    
    
    @driver_required
    def put(self, ride_id):
        """Update a particular ride"""
        kwargs = self.reqparse.parse_args()

        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        driver_id = data['id']

        result = models.Ride.update_ride(ride_id, driverid=driver_id, **kwargs)
        if result != {"message" : "ride does not exist"}:
            return make_response(jsonify(result), 200)
        return make_response(jsonify(result), 404)
    
    @driver_admin_required
    def delete(self, ride_id):
        """Delete a particular ride"""
        result = models.Ride.delete_ride(ride_id)
        if result != {"message" : "the ride does not exist"}:
            return make_response(jsonify(result), 200)
        return make_response(jsonify(result), 404)

class RequestRide(Resource):


    @user_required
    def post(self, ride_id):
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        user_id = data['id']

        result = models.Requests.request_ride(ride_id=ride_id, user_id=user_id)
        return make_response(jsonify(result), 201)


class RequestList(Resource):


    @driver_admin_required
    def get(self):
        """Gets all requests"""
        return make_response(jsonify(models.all_requests), 200)


class Request(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single request"""


    @user_required
    def get(self, request_id):
        """Get a particular request"""
        try:
            ride = models.all_requests[request_id]
            return make_response(jsonify(ride), 200)
        except KeyError:
            return make_response(jsonify({"message" : "specified request does not exist"}), 404)

    @driver_required
    def put(self, request_id):
        """accept/reject a particular request"""

        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        driver_id = data['id']


        result = models.all_requests.get(request_id)
        if result != None:
            if models.all_rides[result["ride_id"]]["driver_id"] == driver_id:
                update = models.Requests.update_request(request_id)
                return make_response(jsonify(update), 200)
            return make_response(jsonify({"message" : "the ride request you are updating is not of your ride"}), 404)
        return make_response(jsonify({"message" : "the ride request does not exist"}), 404)
        
    @user_required
    def delete(self, request_id):
        """Delete a particular request"""

        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        currentuser_id = data['id']

        result = models.all_requests.get(request_id)
        if result != None:
            if result["user_id"] == currentuser_id:
                delete = models.Requests.delete_request(request_id)
                return make_response(jsonify(delete), 200)
            return make_response(jsonify({"message" : "the ride request you are deleting is not your request"}), 404)
        return make_response(jsonify({"message" : "the ride request does not exist"}), 404)
        

rides_api = Blueprint('resources.rides', __name__)
api = Api(rides_api)
api.add_resource(RideList, '/rides', endpoint='rides')
api.add_resource(Ride, '/rides/<int:ride_id>', endpoint='ride')
api.add_resource(RequestRide, '/rides/<int:ride_id>/requests', endpoint='requestride')
api.add_resource(RequestList, '/requests', endpoint='requests')
api.add_resource(Request, '/requests/<int:request_id>', endpoint='request')
