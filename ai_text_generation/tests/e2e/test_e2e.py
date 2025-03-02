from flask import url_for
from unittest.mock import patch


def test_new_registered_user_can_login(client):
    """
    Test that a new registered user can login
    """
    USER = {"username": "new_user", "password": "new_password"}
    with client.application.test_request_context():
        # Register a new user
        register_url = url_for("auth.register")
        register_response = client.post(register_url, json=USER)
        assert register_response.status_code == 201

        # Login with the new user
        login_url = url_for("auth.login")
        login_response = client.post(login_url, json=USER)
        assert login_response.status_code == 200
        assert login_response.json.get("data").get("token") is not None


@patch("app.services.ai_service.ai_service.get_response")
def test_end_to_end(mock_ai_service, client):
    """
    Test end to end
    """
    USER = {"username": "e2e_user", "password": "new_password"}
    MOCK_AI_RESPONSE = "this is a mock response for the AI model"
    mock_ai_service.return_value = MOCK_AI_RESPONSE
    with client.application.test_request_context():
        # Register a new user
        register_url = url_for("auth.register")
        register_response = client.post(register_url, json=USER)
        assert register_response.status_code == 201

        # Login with the new user
        login_url = url_for("auth.login")
        login_response = client.post(login_url, json=USER)
        assert login_response.status_code == 200
        assert login_response.json.get("data").get("token") is not None
        headers = {"Authorization": f"Bearer {login_response.json.get("data").get("token")}"}

        # Generate a new text
        gen_text_url = url_for("textgen.TextGenResource")
        gen_text_response = client.post(gen_text_url, json={"prompt": "hello, generate a physics fact"}, headers=headers)
        assert gen_text_response.status_code == 201
        assert gen_text_response.json.get("response")== MOCK_AI_RESPONSE
        ID = gen_text_response.json.get("id")

        # Update the prompt
        text_by_id_url = url_for("textgen.TextGenByIdResource", id=ID) 
        update_text_response = client.put(text_by_id_url, json={"prompt": "hello, generate a different physics fact"}, headers=headers)
        assert update_text_response.status_code == 200
        assert update_text_response.json.get("response") == MOCK_AI_RESPONSE

        # Get the updated text
        get_text_response = client.get(text_by_id_url, headers=headers)
        assert get_text_response.status_code == 200
        assert get_text_response.json.get("response") == MOCK_AI_RESPONSE

        # Delete the text
        delete_text_response = client.delete(text_by_id_url, headers=headers)
        assert delete_text_response.status_code == 200
        


