from flask import url_for
import pytest
from .test_config import TestConfig
from flask_jwt_extended import create_access_token
from app import create_app, db
from app.models import User

@pytest.fixture
def test_app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(test_app):
    with test_app.test_client() as client:
        return client

@pytest.fixture
def db_session(test_app):
    with test_app.app_context():
        yield db.session
        db.session.rollback()


@pytest.fixture
def test_user(db_session):
    user = User(username="existing_user")
    user.set_password("correct_password")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def auth_header(test_user):
    token = create_access_token(identity=test_user.id)
    return {"Authorization": f"Bearer {token}"}

