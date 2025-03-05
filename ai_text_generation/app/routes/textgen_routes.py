import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.repositories.generated_text_repository import GeneratedTextRepository
from app.services.ai_service import ai_service
from .schemas.textgen_schema import GenerateTextSchema
from app.utils.utils import error_response, response
import logging

logger = logging.getLogger(__name__)
text_gen = Blueprint("textgen", __name__, description="Text Generation")


@text_gen.route("/")
class TextGenResource(MethodView):
    @jwt_required()
    @text_gen.arguments(GenerateTextSchema)
    @text_gen.response(201, GenerateTextSchema)
    def post(self, data):
        logger.info("Generating text")
        user_id = get_jwt_identity()
        prompt = data.get("prompt")
        try:
            response = ai_service.get_response(prompt)
            new_text = GeneratedTextRepository.create_generated_text(user_id=user_id, prompt=prompt, response=response)
            logger.info(f"successfully generated text {new_text.id}")
            return new_text
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            return error_response(str(e), status=500)
    


@text_gen.route("/<string:id>")
class TextGenByIdResource(MethodView):
    @jwt_required()
    @text_gen.response(200, GenerateTextSchema)
    def get(self, id):
        logger.info(f"get text by id: {id}")
        user_id = get_jwt_identity()
        text = GeneratedTextRepository.get_user_generated_texts_by_id(id=id, user_id=user_id)
        if not text:
            logger.error(f"text not found: {id}")
            return error_response("text not found", status=404)
        return text

    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()
        text = GeneratedTextRepository.get_user_generated_texts_by_id(id=id, user_id=user_id)
        if not text:
            logger.error(f"text not found: {id}")
            return error_response("text not found", status=404)
        GeneratedTextRepository.delete_generated_text(text)
        logger.info(f"deleted text:{id}")
        return response(data=None,status=200)

    @jwt_required()
    @text_gen.arguments(GenerateTextSchema)
    @text_gen.response(200, GenerateTextSchema)
    def put(self, data, id):
        user_id = get_jwt_identity()
        text = GeneratedTextRepository.get_user_generated_texts_by_id(id=id, user_id=user_id)
        if not text:
            return error_response("text not found", status=404)
        prompt = data.get("prompt")
        try:
            response = ai_service.get_response(prompt)
            text.prompt, text.response, text.timestamp = prompt, response, db.func.current_timestamp()
            GeneratedTextRepository.update_generated_text(text)
            logger.info(f"updated text: {text.id}")
            return text
        except Exception as e:
            logger.error(f"Error updating text: {str(e)}")
            return error_response(str(e), status=500)




