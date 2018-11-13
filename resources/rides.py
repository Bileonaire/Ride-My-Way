"""Contains all endpoints to manipulate ride information
"""
from flask import request, jsonify, Blueprint, make_response
from flask_restful import Resource, Api, reqparse
import jwt
import psycopg2
# pylint: disable=W0612

import models
import config
from .auth import user_required, admin_required, user_id_required
from databasesetup import db

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
            'numberplate',
            required=True,
            default="0",
            location=['form', 'json'])
        self.reqparse.add_argument(
            'maximum',
            required=True,
            type=int,
            help="kindly provide a valid integer of the maximum number of passengers",
            location=['form', 'json'])
        super().__init__()

    @user_id_required
    def post(self, user_id):
        """Adds a new ride"""
        kwargs = self.reqparse.parse_args()
        driver_id = str(user_id)

        db_cursor = db.con()
        db_cursor.execute("SELECT * FROM rides WHERE driver_id=%s and departuretime=%s and status=%s",
                         (driver_id, kwargs.get("departuretime"),"pending",))
        ride = db_cursor.fetchone()

        if ride != None:
            return make_response(jsonify({"message" : "you will be on another ride at that time"}), 400)

        ride = kwargs.get("departurepoint") + " to " + kwargs.get("destination")
        result = models.Ride.create_ride(ride=ride,
                                         driver_id=driver_id,
                                         departuretime=kwargs.get("departuretime"),
                                         numberplate=kwargs.get("numberplate"),
                                         maximum=str(kwargs.get("maximum")))
        return result

    def get(self):
        """Gets all rides"""
        return models.Ride.get_all_rides()


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
            'numberplate',
            required=False,
            location=['form', 'json'])
        self.reqparse.add_argument(
            'maximum',
            required=True,
            type=int,
            help="kindly provide a valid number of maximum passengers",
            location=['form', 'json'])
        super().__init__()

    def get(self, ride_id):
        """Get a particular ride"""
        return models.Ride.get_ride(ride_id)


    @user_id_required
    def post(self, ride_id, user_id):
        """start a particular ride"""
        driver_id = user_id

        result = models.Ride.start_ride(ride_id=ride_id, driver_id=driver_id)
        if result == {"message" : "ride has started"}:
            return make_response(jsonify(result), 200)
        return make_response(jsonify(result), 404)

    @user_id_required
    def put(self, ride_id, user_id):
        """Update a particular ride"""
        kwargs = self.reqparse.parse_args()

        driver_id = user_id
        db_cursor = db.con()
        db_cursor.execute("SELECT * FROM rides WHERE ride_id=%s", (ride_id,))
        ride = db_cursor.fetchall()

        if ride == []:
            return make_response(jsonify({"message" : "ride does not exist"}), 404)

        ride = kwargs.get("departurepoint") + " to " +kwargs.get("destination")
        result = models.Ride.update_ride(ride_id=ride_id,
                                         ride=ride,
                                         driver_id=driver_id,
                                         departuretime=kwargs.get("departuretime"),
                                         numberplate=kwargs.get("numberplate"),
                                         maximum=kwargs.get("maximum"))
        return result

    @user_required
    def delete(self, ride_id):
        """Delete a particular ride"""
        result = models.Ride.delete_ride(ride_id)
        return result

class RequestRide(Resource):
    """Contains POST method for requsting a particular ride"""


    @user_id_required
    def post(self, ride_id, user_id):
        """Request a particular ride"""
        result = models.Request.request_ride(ride_id=ride_id, user_id=user_id)
        return result

    @user_required
    def get(self, ride_id):
        """get a particular ride requests"""
        result = models.Request.get_particular_riderequests(ride_id=ride_id)
        return result


class RequestList(Resource):
    """Contains GET method to get all requests"""

    @admin_required
    def get(self):
        """Gets all requests"""
        result = models.Request.get_all_requests()
        return result


class Request(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single request"""


    @user_required
    def get(self, request_id):
        """Get a particular request"""
        result = models.Request.get_requests(request_id)
        return result

    @user_id_required
    def put(self, request_id, user_id):
        """accept/reject a particular request"""
        db_cursor = db.con()
        db_cursor.execute("SELECT * FROM request WHERE request_id=%s", (request_id,))
        requesti = db_cursor.fetchall()

        if requesti == []:
            return make_response(jsonify({"message" : "request does not exist"}), 404)

        driver_id = models.Relation.get_driver_id(request_id)
        if type(driver_id) == int and driver_id == int(user_id):
            requesti=requesti[0]
            ride_id = requesti[2]
            if requesti[4] == True:
                db_cursor = db.con()
                db_cursor.execute("UPDATE request SET accepted=%s WHERE request_id=%s",
                                    (False, request_id))
                db.commit()
                return make_response(jsonify({"message" : "request has been rejected"}), 200)

            db_cursor.execute("SELECT * FROM request WHERE ride_id=%s and accepted=%s", (ride_id,True,))
            accepted = db_cursor.fetchall()
            total = len(accepted)
            maximum = models.Relation.get_maximum(request_id)

            if int(total) < int(maximum):
                update = models.Request.accept_request(request_id)
                return update
            return make_response(jsonify({"message" : "maximum requests have been accepted"}), 400)
        return make_response(jsonify({"message" : "the request is not of your ride"}), 400)


    @user_id_required
    def delete(self, request_id, user_id):
        """Delete a particular request"""
        currentuser_id = user_id

        db_cursor = db.con()
        db_cursor.execute("SELECT * FROM request WHERE request_id=%s", (request_id,))
        request = db_cursor.fetchone()

        if request != None:
            if currentuser_id == request[1]:
                delete = models.Request.delete_request(request_id)
                return delete
            return make_response(jsonify({"message" : "the request is not yours"}), 400)
        return make_response(jsonify({"message" : "request does not exists"}), 404)

class Slack(Resource):
    """Contains Post methods for slack"""

    def post(self):
        """start a particular ride"""
        result = {"message": {"text": 'Would you like to play a game?',
   "attachments": [{
       "text": 'Choose a game to play',
       "fallback": 'You are unable to choose a game',
       "callback_id": 'wopr_game',
       "color": '#3AA3E3',
       "attachment_type": 'default',
       "actions": [
         {
           "name": 'game',
           "text": 'Chess',
           "type": 'button',
           "value": 'chess'
         },
         {
           "name": 'game',
           "text": "Falken's Maze",
           "type": 'button',
           "value": 'maze'
         },
         {
           "name": 'game',
           "text": 'Thermonuclear War',
           "style": 'danger',
           "type": 'button',
           "value": 'war',
           "confirm": {
             "title": 'Are you sure?',
             "text": "Wouldn't you prefer a good game of chess?",
             "ok_text": 'Yes',
             "dismiss_text": 'No'
           }
         }
       ]
     }
   ]
 }
}
        return make_response(jsonify(result), 404)


rides_api = Blueprint('resources.rides', __name__)
api = Api(rides_api)
api.add_resource(RideList, '/rides', endpoint='rides')
api.add_resource(Ride, '/rides/<int:ride_id>', endpoint='ride')
api.add_resource(RequestRide, '/rides/<int:ride_id>/requests', endpoint='requestride')
api.add_resource(RequestList, '/requests', endpoint='requests')
api.add_resource(Request, '/requests/<int:request_id>', endpoint='request')
api.add_resource(Slack, '/slack', endpoint='slack')
