# tests/test_config.py
import os

class TestConfig:
    API_TITLE = "AI Text Generation"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test_secret_key"

