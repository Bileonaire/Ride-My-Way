"""Contain interactive documentation to help one get started using the API
"""
import os

from flasgger import Swagger

from app import create_app


app = create_app('config.ProductionConfig')
swagger = Swagger(app)


# Users
@app.route('/api/v1/auth/userregister', methods=["POST"])
def signup():
    """ endpoint for registering users.
    ---
    parameters:
      - name: username
        required: true
        in: formData
        type: string
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
      - name: confirm_password
        in: formData
        type: string
        required: true
    """

@app.route('/api/v1/auth/login', methods=["POST"])
def login():
    """ endpoint for logging in users.
    ---
    parameters:
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: password
        required: true
    """

@app.route('/api/v1/auth/driverregister', methods=["POST"])
def Driversignup():
    """ endpoint for registering users.
    ---
    parameters:
      - name: username
        required: true
        in: formData
        type: string
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
      - name: confirm_password
        in: formData
        type: string
        required: true
      - name: carmodel
        in: formData
        type: string
        required: true
      - name: numberplate
        in: formData
        type: string
        required: true
    """


@app.route('/api/v1/users', methods=["POST"])
def users_create():
    """ endpoint for creating users.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: username
        required: true
        in: formData
        type: string
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
      - name: confirm_password
        in: formData
        type: string
        required: true
      - name: usertype
        in: formData
        type: string
        required: false
        default: user
      - name: carmodel
        in: formData
        type: string
        required: false
      - name: numberplate
        in: formData
        type: string
        required: false
    """

@app.route("/api/v1/users", methods=["GET"])
def get_all_users():
    """endpoint for  getting all users.
     ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
    """

@app.route("/api/v1/users/<int:user_id>", methods=["GET"])
def get_one_user():
    """endpoint for  getting a particular user.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: user_id
        in: path
        type: integer
        required: true
    """

@app.route('/api/v1/users/<int:user_id>', methods=["PUT"])
def update_user():
    """ endpoint for updating an existing user.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: username
        required: true
        in: formData
        type: string
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
      - name: confirm_password
        in: formData
        type: string
        required: true
      - name: id
        in: path
        type: integer
        required: true
      - name: usertype
        in: formData
        type: string
        required: false
        default: user
      - name: carmodel
        in: formData
        type: string
        required: false
      - name: numberplate
        in: formData
        type: string
        required: false
    """

@app.route('/api/v1/users/<int:user_id>', methods=["DELETE"])
def delete_user():
    """ endpoint for deleting an existing user.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: user_id
        in: path
        type: integer
        required: true
    """


# Ride
@app.route('/api/v1/rides', methods=["POST"])
def create_ride():
    """ endpoint for creating a ride.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: departurepoint
        required: true
        in: formData
        type: string
      - name: destination
        in: formData
        type: string
        required: true
      - name: departuretime
        required: true
        in: formData
        type: string
      - name: cost
        required: true
        in: formData
        type: string
      - name: maximum
        required: true
        in: formData
        type: integer
    """

@app.route("/api/v1/rides", methods=["GET"])
def get_all_rides():
    """endpoint for getting all rides.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: false
    """

@app.route("/api/v1/rides/<int:ride_id>", methods=["GET"])
def get_one_ride():
    """endpoint for  getting a particular ride.
    ---
    parameters:
      - name: ride_id
        in: path
        type: integer
        required: true
    """

@app.route("/api/v1/rides/<int:ride_id>", methods=["POST"])
def start_a_ride():
    """endpoint for  starting a particular ride.
    ---
    parameters:
      - name: ride_id
        in: path
        type: integer
        required: true
      - name: x-access-token
        in: header
        type: string
        required: true
    """

@app.route('/api/v1/rides/<int:ride_id>', methods=["PUT"])
def update_ride():
    """ endpoint for updating an existing ride.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: departurepoint
        required: true
        in: formData
        type: string
      - name: destination
        in: formData
        type: string
        required: true
      - name: departuretime
        required: true
        in: formData
        type: string
      - name: cost
        required: true
        in: formData
        type: string
      - name: maximum
        required: true
        in: formData
        type: integer
      - name: ride_id
        required: true
        in: path
        type: integer

    """

@app.route('/api/v1/rides/<int:ride_id>', methods=["DELETE"])
def delete_ride():
    """ endpoint for deleting an existing ride.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: ride_id
        in: path
        type: integer
        required: true
    """


# request
@app.route('/api/v1/rides/<int:ride_id>/requests', methods=["POST"])
def request_ride():
    """ endpoint for requesting ride.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: ride_id
        required: true
        in: path
        type: string
    """

@app.route("/api/v1/requests", methods=["GET"])
def get_all_requests():
    """endpoint for  getting all requests.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
    """

@app.route("/api/v1/requests/<int:request_id>", methods=["GET"])
def get_one_request():
    """endpoint for getting a particular request.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: request_id
        in: path
        type: integer
        required: true
    """

@app.route('/api/v1/requests/<int:request_id>', methods=["PUT"])
def update_request():
    """ endpoint for accepting/rejecting a request.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: request_id
        required: true
        in: path
        type: string
    """

@app.route('/api/v1/requests/<int:request_id>', methods=["DELETE"])
def delete_borrowed():
    """ endpoint for deleting an existing request.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: request_id
        in: path
        type: integer
        required: true
    """

@app.route('/')
def hello_world():
    "test that flask app is running"
    return "To view the docs visit: https://bileonaireridesv1.herokuapp.com/apidocs"


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run('0.0.0.0', port=port)
