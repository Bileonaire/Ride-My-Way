"""Handles data storage for Users, rides and requests
"""

from werkzeug.security import generate_password_hash


all_users = {1 : {"id": "1", "username" : "admin",
                  "email" : "admin@gmail.com",
                  "password" : generate_password_hash("admin1234", method='sha256'),
                  "usertype" : "admin",
                  "carmodel" : None, "numberplate" : None},}
user_count = 2

all_rides = {}
ride_count = 1

all_requests = {}
request_count = 1

class User(object):
    """Contains methods to add, update and delete a user"""


    @staticmethod
    def create_user(username, email, password, usertype, carmodel=None, numberplate=None):
        """Creates a new user and appends his information to the all_users dictionary"""
        global all_users
        global user_count
        password = generate_password_hash(password, method='sha256')
        all_users[user_count] = {"id": user_count, "username" : username,
                                 "email" : email, "password" : password, "usertype" : usertype,
                                 "carmodel" : carmodel, "numberplate" : numberplate}
        new_user = all_users[user_count]
        user_count += 1
        return new_user


    @staticmethod
    def update_user(user_id, usertype, username, email, password, carmodel=None, numberplate=None):
        """Updates user information"""
        if user_id in all_users.keys():
            all_users[user_id] = {"id" : user_id, "username" : username,
                                  "email" : email, "password" : password,
                                  "carmodel" : carmodel, "numberplate" : numberplate,
                                  "usertype" : usertype}
            return all_users[user_id]
        return {"message" : "user does not exist"}

    @staticmethod
    def delete_user(user_id):
        """Deletes a user"""
        try:
            del all_users[user_id]
            return {"message" : "user successfully deleted"}
        except KeyError:
            return {"message" : "user does not exist"}

    @staticmethod
    def all_users():
        """get all users"""

        users = []
        for user in all_users:
            user = all_users[user]

            if user["usertype"] == "driver":
                profile = {user['id'] : {"Username" : user['username'], "Email" : user['email'],
                                         "Usertype" : user['usertype'],
                                         "Car Model" : user["carmodel"],
                                         "Number Plate" : user["numberplate"],
                                         "Rides already given" : [], "Rides pending" : []}}
                for ride in all_rides:
                    ride = all_rides[ride]
                    if ride["driver_id"] == user["id"]:
                        if ride["status"] == "given":
                            profile[user['id']]["Rides already given"].append(ride["trip"])
                        profile[user['id']]["Rides pending"].append(ride["trip"])
            else:
                profile = {user['id'] : {'username' : user['username'], 'email' : user['email'],
                                         'usertype' : user['usertype'],
                                         'Rides already taken' : [],
                                         'Rides pending' : [], 'Rides rejected' : []}}
                for request in all_requests:
                    request = all_requests[request]
                    if request["user_id"] == user["id"]:
                        triprequest = all_rides[request["ride_id"]]["trip"]
                        if request["status"] == "taken":
                            profile[user['id']]["Rides already taken"].append(triprequest)
                        if request["status"] == "pending":
                            profile[user['id']]["Rides pending"].append(triprequest)
                        if request["status"] == "rejected":
                            profile[user['id']]["Rides rejected"].append(triprequest)

            users.append(profile)

        return {"all_users" : users}

    @staticmethod
    def get_user(user_id):
        """get a user"""

        user = all_users[user_id]

        if user["usertype"] == "driver":
            profile = {user['id'] : {"Username" : user['username'], "Email" : user['email'],
                                     "Usertype" : user['usertype'],
                                     "Car Model" : user["carmodel"],
                                     "Number Plate" : user["numberplate"],
                                     "Rides already given" : [], "Rides pending" : []}}

            for ride in all_rides:
                ride = all_rides[ride]
                if ride["driver_id"] == user_id:
                    if ride["status"] == "given":
                        profile[user['id']]["Rides already given"].append(ride["trip"])
                    profile[user['id']]["Rides pending"].append(ride["trip"])
                return profile

        else:
            profile = {user['id'] : {"username" : user['username'], "email" : user['email'],
                                     "usertype" : user['usertype'],
                                     "Rides already taken" : [], "Rides pending" : [],
                                     "Rides rejected" : []}}
            for request in all_requests:
                request = all_requests[request]
                if request["user_id"] == user_id:
                    triprequest = all_rides[request["ride_id"]]["trip"]
                    if request["status"] == "taken":
                        profile[user['id']]["Rides already taken"].append(triprequest)
                    if request["status"] == "pending":
                        profile[user['id']]["Rides pending"].append(triprequest)
                    if request["status"] == "rejected":
                        profile[user['id']]["Rides rejected"].append(triprequest)
                return profile
        return profile



class Ride(object):
    """Contains methods to add, update and delete a ride"""


    @staticmethod
    def create_ride(departurepoint, destination, driverid, departuretime, cost,
                    maximum, status="pending"):
        """Creates a ride and appends this information to rides dictionary"""
        global all_rides
        global ride_count
        all_rides[ride_count] = {"id": ride_count, "trip" : departurepoint + " to " + destination,
                                 "driver_id": driverid, "departuretime": departuretime,
                                 "cost": cost, "maximum": maximum,
                                 "passengers" : [], "status" : status}
        new_ride = all_rides[ride_count]
        ride_count += 1
        return new_ride

    @staticmethod
    def update_ride(ride_id, departurepoint, destination, driverid, departuretime, cost, maximum):
        """Updates ride information"""

        if ride_id in all_rides.keys():
            passengers = all_rides[ride_id]["passengers"]
            status = all_rides[ride_id]["status"]
            all_rides[ride_id] = {"id": ride_id, "trip" : departurepoint + " to " + destination,
                                  "driver_id": driverid, "departuretime": departuretime,
                                  "cost": cost, "maximum": maximum,
                                  "passengers": passengers, "status" : status}
            return all_rides[ride_id]
        return {"message" : "ride does not exist"}

    @staticmethod
    def start_ride(ride_id, driver_id):
        """starts a ride"""

        if ride_id in all_rides.keys():

            if all_rides[ride_id]["driver_id"] == driver_id:
                all_rides[ride_id]["status"] = "given"

                for request in all_requests:
                    request = all_requests[request]
                    if request["ride_id"] == ride_id:
                        if request["accepted"] is True:
                            request["status"] = "taken"
                        elif request["accepted"] is False:
                            request["status"] = "rejected"

                return {"message" : "ride has started"}

            return {"message" : "The ride you want to start is not your ride."}
        return {"message" : "ride does not exist"}

    @staticmethod
    def delete_ride(ride_id):
        """Deletes a ride"""
        try:
            del all_rides[ride_id]
            for request in all_requests:
                request = all_requests[request]
                if request["ride_id"] == ride_id:
                    request["status"] = "ride deleted"

            return {"message" : "the ride successfully deleted"}
        except KeyError:
            return {"message" : "the ride does not exist"}


class Requests(object):
    """Contains methods to add, update and delete requests"""


    @staticmethod
    def request_ride(ride_id, user_id, accepted=False, status="pending"):
        """Creates a new request and appends this information to the all_requests dictionary"""
        global all_requests
        global request_count
        all_requests[request_count] = {"id": request_count, "ride_id" : ride_id, "user_id": user_id,
                                       "accepted": accepted, "status" : status}
        request_count += 1

        return {"message" : "the request has been sent for approval"}

    @staticmethod
    def update_request(request_id):
        """Updates request information in all_requests dictionary"""
        maximum = int(all_rides[all_requests[request_id]["ride_id"]]["maximum"])
        accepted = all_rides[all_requests[request_id]["ride_id"]]["passengers"]
        passengers = int(len(accepted))

        if passengers < maximum:
            if all_requests[request_id]["accepted"] is False:
                all_requests[request_id]["accepted"] = True
                accepted.append(all_users[all_requests[request_id]["user_id"]]["username"])
                return {"message" : "the request has been accepted"}

            elif all_requests[request_id]["accepted"] is True:
                all_requests[request_id]["accepted"] = False
                accepted.remove(all_users[all_requests[request_id]["user_id"]]["username"])
                return {"message" : "the request has been rejected"}
        else:
            if all_requests[request_id]["accepted"] is True:
                all_requests[request_id]["accepted"] = False
                accepted.remove(all_users[all_requests[request_id]["user_id"]]["username"])
                return {"message" : "the request has been rejected"}
            return {"message" : "the ride has reached its maximum number of passengers"}

    @staticmethod
    def delete_request(request_id):
        """Deletes a request from the all request dictionary"""
        try:
            del all_requests[request_id]
            return {"message" : "request successfully deleted"}
        except KeyError:
            return {"message" : "the specified request does not exist in requests"}
