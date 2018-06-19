"""Creates app instance, registers Blueprints and runs the Flask application
"""
import os

from flask import Flask

from resources.rides import rides_api
from resources.users import users_api


def create_app(configuration):
    """Creates the flask app"""

    app = Flask(__name__)
    app.config.from_object(configuration)
    app.url_map.strict_slashes = False

    app.register_blueprint(rides_api, url_prefix='/api/v1')
    app.register_blueprint(users_api, url_prefix='/api/v1')

    return app

app = create_app('config.ProductionConfig')


@app.route('/')
def hello_world():
    """Tests running of the flask app"""
    
    return 'Welcome to Ride My Way. Bileonaire Rides'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run('0.0.0.0', port=port)
