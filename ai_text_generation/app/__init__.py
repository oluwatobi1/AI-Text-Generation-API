from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_smorest import Api

db = SQLAlchemy()

jwt = JWTManager()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    api = Api(app)
    
    @app.route("/")
    def home():
        return "<h3>AI Text Generation</h3></br><h3>Visit  <a href='/swagger-ui'>Swagger</a>  documentation</h3>"
    
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    from app.routes.auth_routes import auth
    from app.routes.textgen_routes import text_gen
    api.register_blueprint(auth, url_prefix="/auth")
    api.register_blueprint(text_gen, url_prefix="/generate-text")
    return app