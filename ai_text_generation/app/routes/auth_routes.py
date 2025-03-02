from flask_smorest import Blueprint
from flask_jwt_extended import create_access_token
from app.models import User
from app import db

from app.utils.utils import response, error_response, custom_response
from .schemas.auth_schema import UserSchema
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@auth.route("/login", methods=["POST"])
@auth.arguments(UserSchema)
def login(data):
    user, password = data.get("username"), data.get("password")
    user = User.query.filter_by(username=user).first()

    if user and user.check_password(password):
        token = create_access_token(identity=user.id)
        return response(data={"username": user.username, "token": token})
    return error_response("invalid username or password", status=401)

# @auth.route("/users", methods=["GET"])
# @auth.response(200, UserSchema(many=True))
# def get_all_users():
#     users = User.query.all()

#     return response(data=UserSchema(many=True).dump(users))
