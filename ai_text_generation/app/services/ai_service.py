from app.config import Config
from langchain.chat_models import init_chat_model

class AIService:
  def __init__(self):
    self.model = init_chat_model(Config.AI_MODEL_NAME, model_provider=Config.AI_MODEL_PROVIDER)
  
  def get_response(self, prompt):
    return self.model.invoke(prompt).content


# Singleton instance (Created only once)
ai_service = AIService()