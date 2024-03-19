from datetime import datetime

from ReportApp import app, db  # Assuming your Flask app instance is named 'app'
from flask import Flask
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_login import LoginManager, login_user
from flask_security import UserMixin, RoleMixin

# import required libraries from flask_login and flask_security

from flask_login import LoginManager, login_manager, login_user

from flask_security import Security, SQLAlchemySessionUserDatastore

from flask_wtf import FlaskForm

from flask_wtf.file import FileField, FileRequired

from wtforms import validators



# storing type of roles e.g staff and student
class RoleType(db.Model, RoleMixin):
    __tablename__ = 'roletype'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)


# create table in database for assigning roles base on user
roles_netusers = db.Table('roles_netusers ',
                       db.Column('netuser_id', db.Integer(), db.ForeignKey('netuser.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('roletype.id')))


# storing all users
class NetUsers(db.Model, UserMixin):
    __tablename__ = 'netuser'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Name = db.Column(db.String)
    Surname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean())
    # backreferences the user_id from roles_users table
    roles = db.relationship('RoleType', secondary=roles_netusers, backref='roled')

class Report(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    Name = db.Column(db.String)
    Surname = db.Column(db.String)
    date_field = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String)
    Location = db.Column(db.String)
    info = db.Column(db.String)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('netuser.id'), nullable=True)



# creates all database tables
@app.before_first_request
def create_tables():
    db.create_all()




# load users, roles for a session
user_datastore = SQLAlchemySessionUserDatastore(db.session, NetUsers, RoleType)
security = Security(app, user_datastore)

