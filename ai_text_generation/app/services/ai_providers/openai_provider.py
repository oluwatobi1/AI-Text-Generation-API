
from app.config import Config
from langchain.chat_models import init_chat_model
from app.services.ai_providers.base import AIProvider

class OpenAIProvider(AIProvider):
  def __init__(self):
    self.model = init_chat_model(Config.AI_MODEL_NAME, model_provider=Config.AI_MODEL_PROVIDER)
  
  def get_response(self, prompt):
    return self.model.invoke(prompt).content
