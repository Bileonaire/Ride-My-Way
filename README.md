[![Build Status](https://travis-ci.org/Bileonaire/Ride-My-Way.svg?branch=Develop-V1-API)](https://travis-ci.org/Bileonaire/Ride-My-Way)
[![Coverage Status](https://coveralls.io/repos/github/Bileonaire/Ride-My-Way/badge.svg?branch=Develop-V1-API)](https://coveralls.io/github/Bileonaire/Ride-My-Way?branch=Develop-V1-API)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

# Ride My Way Bileonaire Rides
Bileonaire Rides is a carpooling application that provides drivers with the ability to create ride oﬀers  and passengers to join available ride oﬀers. 

![Home Image](https://raw.github.com/Bileonaire/Ride-My-Way/Develop-V1-API/bileonaire.jpg)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Git
* Python 3.6.4
* Virtualenv

### Quick Start

1. Clone the repository

```
$ git clone https://github.com/Bileonaire/Leon-Library.git
$ cd into the created folder
```
  
2. Initialize and activate a virtualenv

```
$ virtualenv --no-site-packages env
$ source env/bin/activate
```

3. Install the dependencies

```
$ pip install -r requirements.txt
```

4. Initialize environment variables

```
$ export SECRET_KEY=<SECRET KEY>
```

5. Run the development server

```
$ python app.py
```

6. Navigate to [http://localhost:5000](http://localhost:5000)

At the / endpoint you should see Welcome to library books API displayed in your browser.

## Endpoints

Here is a list of all endpoints in the Bileonaire Rides API

Endpoint | Functionality 
------------ | -------------
POST   /api/v1/auth/userregister | Register a user
POST   /api/v1/auth/driverregister | Register a driver
POST   /api/v1/auth/login | Log in user
POST   /api/v1/users | Create a user
GET    /api/v1/users | Get all users
GET   /api/v1/users/id | Get a single user
PUT  /api/v1/users/id | Update a single user
DELETE   /api/v1/users/id | Delete a single user
POST   /api/v1/rides | Create new ride
GET   /api/v1/rides | Get all rides
GET   /api/v1/rides/id | Get a single ride
PUT   /api/v1/rides/id | Update a single ride
POST   /api/v1/rides/id/ | Start a ride
DELETE   /api/v1/rides/id | Delete a single ride
POST   /api/v1/rides/id/requests | Request a ride
GET   /api/v1/requests | Get all requests
DELETE   /api/v1/requests/id | Delete a single request
GET   /api/v1/requests/id | Get a single request
PUT  /api/v1/requests/id | Accept/Reject a request

## Running the tests

To run the automated tests simply run

```
nosetests tests
```

### And coding style tests

Coding styles tests are tests that ensure conformity to coding style guides. In our case, they test conformity to
PEP 8 style guides

```
pylint app.py
```

## Deployment

Ensure you use Productionconfig settings which have DEBUG set to False

## Built With

* HTML5
* CSS3
* Python 3.6.4
* Flask - The web framework used

## GitHub pages

https://Bileonaire.github.io/

## Heroku

https://bileonaireridesv1.herokuapp.com/apidocs

## Versioning

Most recent version is version 1

## Authors

Bileonaire Leon.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration and encouragement
* etc
