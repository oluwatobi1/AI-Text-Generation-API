import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import GeneratedText
from app.services.ai_service import ai_service
from .schemas.textgen_schema import GenerateTextSchema,ErrSchema
from app.utils.utils import error_response, response
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

text_gen = Blueprint("textgen", __name__, description="Text Generation")


@text_gen.route("/")
class TextGenResource(MethodView):
    @jwt_required()
    @text_gen.arguments(GenerateTextSchema)
    @text_gen.response(201, GenerateTextSchema)
    def post(self, data):
        user_id = get_jwt_identity()
        prompt = data.get("prompt")
        try:
            response = ai_service.get_response(prompt)
            new_text = GeneratedText(user_id=user_id, prompt=prompt, response=response)
            db.session.add(new_text)
            db.session.commit()
            logger.info(f"successfully generated text {new_text.id}")
            return new_text
        except Exception as e:
            return error_response(str(e), status=500)
    
    @text_gen.response(200, GenerateTextSchema(many=True))
    def get(self):
        g = GeneratedText.query.all()

        return g


@text_gen.route("/<id>")
class TextGenByIdResource(MethodView):
    @jwt_required()
    @text_gen.response(200, GenerateTextSchema)
    def get(self, id):
        user_id = get_jwt_identity()
        print("user_id", user_id, "id", id)
        text = GeneratedText.query.filter_by(id=id, user_id=user_id).first()
        if not text:
            return error_response("text not found", status=404)
        return text

    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()
        text = GeneratedText.query.filter_by(id=id, user_id=user_id).first()
        if not text:
            return error_response("text not found", status=404)
        db.session.delete(text)
        db.session.commit()
        return response(data=None,status=200)

    @jwt_required()
    @text_gen.arguments(GenerateTextSchema)
    @text_gen.response(200, GenerateTextSchema)
    def put(self, data, id):
        user_id = get_jwt_identity()
        text = GeneratedText.query.filter_by(id=id, user_id=user_id).first()
        if not text:
            return error_response("text not found", status=404)
        prompt = data.get("prompt")
        try:
            response = ai_service.get_response(prompt)
            text.prompt, text.response, text.timestamp = prompt, response, db.func.current_timestamp()
            db.session.commit()
            return text
        except Exception as e:
            return error_response(str(e), status=500)




