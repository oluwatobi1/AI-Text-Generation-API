from flask import request
from flask_smorest import Blueprint
from app.models import User
from app import db

from app.utils.utils import response, error_response
from .schemas.auth import UserSchema

auth = Blueprint('auth', __name__, description="Authentication")


@auth.route("/register", methods= ["POST"])
@auth.arguments(UserSchema)
@auth.response(201, UserSchema)
def register(data):
    username, password = data.get("username"), data.get("password")
    if User.query.filter_by(username=username).first():
        return error_response("username already exists")


    new_user = User(username=username)
    new_user.set_password(password=password)
    db.session.add(new_user)
    db.session.commit()
    return response(data={"username": new_user.username}, status=201)