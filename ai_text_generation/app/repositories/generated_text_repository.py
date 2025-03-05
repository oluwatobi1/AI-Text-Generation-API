from app.models import GeneratedText, db


class GeneratedTextRepository:
    @staticmethod
    def create_generated_text(user_id, prompt, response):
        generated_text = GeneratedText(user_id=user_id, prompt=prompt, response=response)
        db.session.add(generated_text)
        db.session.commit()
        return generated_text

    @staticmethod
    def get_user_generated_texts_by_id(id, user_id):
        return GeneratedText.query.filter_by(id=id, user_id=user_id).first()


    @staticmethod
    def delete_generated_text(text):
        db.session.delete(text)
        db.session.commit()
        return True
    
    @staticmethod
    def update_generated_text(new_response):
        text = GeneratedText.query.get_or_404(new_response.id)
        text.prompt = new_response.prompt
        text.response = new_response.response
        text.timestamp = db.func.current_timestamp()
        db.session.commit()
        return text



