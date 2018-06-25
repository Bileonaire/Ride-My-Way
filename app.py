"""Creates app instance, registers Blueprints and runs the Flask application
"""
import os
import datetime

from flask import Flask

from resources.users import users_api
from resources.rides import rides_api

from models import db


def create_app(configuration):
    """Create flask app"""
    app = Flask(__name__)
    app.config.from_object(configuration)
    app.url_map.strict_slashes = False

    app.register_blueprint(users_api, url_prefix='/api/v2')
    app.register_blueprint(rides_api, url_prefix='/api/v2')
    db.init_app(app)

    return app

app = create_app('config.ProductionConfig')


@app.route('/')
def hello_world():
    "test that flask app is running"
    days = {0 : "Monday", 1 : "Tuesday", 2 : "Wednesday", 3 : "Thursday", 4: "Friday"}
    today = datetime.datetime.combine(datetime.date.today(), datetime.time())
           #datetime.datetime.combine(datetime.date.today(), datetime.time())
    if today.weekday() <= 4:
        leo = (days[today.weekday()])
        return "welcome to Bileonaire Rides this " + leo
    return "Sorry, we are not open on weekends."
    


if __name__ == '__main__':
    app.run()
    # port = int(os.environ.get('PORT', 5000))
    # app.run('', port=port)
