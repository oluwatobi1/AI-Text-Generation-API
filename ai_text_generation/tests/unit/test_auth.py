import pytest
from flask import url_for
from app.models import User

register_test_cases = [
     pytest.param({"username": "user1", "password":"sample_password"}, 201, "user1", id="REGISTER:VALID_USER"),
     pytest.param({"username": "", "password":"sample_password"}, 422, None, id="REGISTER:EMPTY_USERNAME"),
     pytest.param({"username": "user1", "password":""}, 422, None, id="REGISTER:EMPTY_PASSWORD"),
]



@pytest.mark.parametrize("user_test, expected_status, expected_value", register_test_cases)
def test_register(client,  user_test, expected_status, expected_value):
    with client.application.test_request_context():
        url = url_for("auth.register")
        response = client.post(url, json=user_test)
        assert response.status_code == expected_status

        if expected_value:
            assert response.json.get("data").get("username") == expected_value
            assert User.query.filter_by(username=expected_value).first() is not None


login_test_cases = [
    pytest.param({"username": "existing_user", "password":"correct_password"}, 200, "existing_user", id="LOGIN:USER", ), # Valid user
    pytest.param({"username": "user1", "password":"wrong_password"}, 401, None, id="LOGIN:WRONG_PASSWORD"), # Wrong password
    pytest.param( {"username": "wrong_user", "password":"sample_password"}, 401, None, id="LOGIN:USER_NOT_EXIST"), # User does not exist
    pytest.param({"username": "", "password": "sample_password"}, 422, None, id="LOGIN:EMPTY_USERNAME"),
    pytest.param({"username": "user1", "password": ""}, 422, None, id="LOGIN:EMPTY_PASSWORD"),

]

@pytest.mark.parametrize("login_data, expected_status, token_expected ", login_test_cases)
def test_login(client,test_user, login_data, expected_status, token_expected):
    with client.application.test_request_context():
        url = url_for("auth.login")
        response = client.post(url, json=login_data)
        print("login_data", login_data, "response", response.json, response.status_code, expected_status, token_expected)
        assert response.status_code == expected_status
        if token_expected:
            assert response.json["data"]["token"] is not None
        else:
            assert "token" not in response.json