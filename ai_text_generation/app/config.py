import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_TITLE = "AI Text Generation"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_RAPIDOC_PATH = "/rapidoc"
    OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"
    OPENAPI_SWAGGER_UI_VERSION = "3.36.0"


    
    SECRET_KEY = os.getenv('SECRET_KEY', "randoem_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "random_jwt_secret_key")

    AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "llama3-8b-8192")
    AI_MODEL_PROVIDER = os.getenv("AI_MODEL_PROVIDER", "groq")
    PORT = os.getenv("PORT", 8000)