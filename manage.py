"""Handles database migrations"""
import re
import sys

from flask_script import Manager, prompt, prompt_pass

import models
from app import app
from databasesetup import db


manager = Manager(app)

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

@manager.command
def createsuperuser():
    """Create a superuser, requires username, email and password."""
    db.tables_creation()

    username = prompt('superuser username')

    email = prompt('superuser email')
    confirm_email = prompt('confirm superuser email')

    if not EMAIL_REGEX.match(email):
        sys.exit('\n kindly provide a valid email address')

    if not email == confirm_email:
        sys.exit('\n kindly ensure that email and confirm email are identical')

    password = prompt_pass('superuser password')
    confirm_password = prompt_pass('confirm superuser password')

    if len(password) < 8:
        sys.exit('\n kindly ensure that the password is at leaast 8 characters long')

    if not password == confirm_password:
        sys.exit('\n kindly ensure that password and confirm password are identical')
    admin = True

    models.User(username=username, email=email, password=password, admin=admin)
    sys.exit('\n superuser successfully created')

if __name__ == '__main__':
    manager.run()

# python manage.py createsuperuser
