import pytest
from app.models import User

register_test_case = [
    ({"username": "user1", "password":"sample_password"}, 201, "user1"),
    ({"username": "", "password":"sample_password"}, 422, None),
    ({"username": "user1", "password":""}, 422, None)
]



@pytest.mark.parametrize("user_test, expected_status, expected_value", register_test_case)
def test_register(client, user_test, expected_status, expected_value):
    response = client.post("/auth/register", json=user_test)
    assert response.status_code == expected_status

    if expected_value:
        assert response.json.get("data").get("username") == expected_value
        assert User.query.filter_by(username=expected_value).first() is not None