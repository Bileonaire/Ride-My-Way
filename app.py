"""Creates app instance, registers Blueprints and runs the Flask application
"""
import os
import datetime

from flask import Flask

from resources.rides import rides_api 
from resources.users import users_api
from databasesetup import db


def create_app(configuration):
    """Create flask app"""
    app = Flask(__name__)
    app.config.from_object(configuration)
    app.url_map.strict_slashes = False

    app.register_blueprint(users_api, url_prefix='/api/v3')
    app.register_blueprint(rides_api, url_prefix='/api/v3')
    db.tables_creation()

    return app

app = create_app('config.TestingConfig')


@app.route('/')
def hello_world():
    "test that flask app is running"
    days = {0 : "Monday", 1 : "Tuesday", 2 : "Wednesday", 3 : "Thursday", 4: "Friday", 5: "Sarturday", 6:"Sunday"}
    today = datetime.datetime.combine(datetime.date.today(), datetime.time())
    day_name = (days[today.weekday()])
    return "welcome to Bileonaire Rides this " + day_name

if __name__ == '__main__':
    app.run()
