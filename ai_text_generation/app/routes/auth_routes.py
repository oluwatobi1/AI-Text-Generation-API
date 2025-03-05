from flask_smorest import Blueprint
from flask import current_app as app
from flask_jwt_extended import create_access_token
from app.models import User
from app import db
from app.utils.utils import response, error_response
from .schemas.auth_schema import UserSchema
import logging


logger = logging.getLogger(__name__)
auth = Blueprint('auth', __name__, description="Authentication")


@auth.route("/register", methods= ["POST"])
@auth.arguments(UserSchema)
@auth.response(201, UserSchema)
def register(data):
    username = data.get("username").lower()
    logger.info(f"Registering new user: {username}")
    password = data.get("password")
    if User.query.filter_by(username=username).first():
        return error_response("username already exists")

    new_user = User(username=username)
    new_user.set_password(password=password)
    db.session.add(new_user)
    db.session.commit()
    logger.info(f"New user created: {new_user.username}")
    return response(data={"username": new_user.username}, status=201)

@auth.route("/login", methods=["POST"])
@auth.arguments(UserSchema)
def login(data):
    username = data.get("username").lower()
    logger.info(f"Logging in user: {username}")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        token = create_access_token(identity=user.id)
        logger.info(f"User logged in: {user.username}")
        return response(data={"username": user.username, "token": token})
    logger.warning(f"Invalid username or password")
    return error_response("invalid username or password", status=401)
