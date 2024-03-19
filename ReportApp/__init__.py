from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import ReportApp

app = Flask(__name__)

# This will create the db file in the instance
# if the database is not present already
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///g4g.sqlite3"
app.config['SECRET_KEY'] = 'Password'
# hashes the password and then stores in the database
app.config['SECURITY_PASSWORD_SALT'] = "Password"
# allows new registrations to application
app.config['SECURITY_REGISTERABLE'] = True
# to send automatic registration email to user
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False


# Create the database
db = SQLAlchemy(app)

# Configure login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # specify the login view
login_manager.login_message_category = 'info'  # specify the category of the flashed message

from ReportApp import views, tables

if __name__ == '__main__':
    ReportApp.run(debug=True)