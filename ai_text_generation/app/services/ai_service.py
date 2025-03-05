from app.config import Config
from langchain.chat_models import init_chat_model
from app.services.ai_providers.openai_provider import OpenAIProvider

# Factory function to get the AI provider
def get_ai_provider():
    provider_map = {
        "openai": OpenAIProvider,
        "groq": OpenAIProvider,
    }
    selected_provider = Config.AI_MODEL_PROVIDER.lower()
    
    if selected_provider not in provider_map:
        raise ValueError(f"Unsupported AI provider: {selected_provider}")
    
    return provider_map[selected_provider]()


class AIService:
    def __init__(self):
        self.provider = get_ai_provider()  
    
    def get_response(self, prompt):
        return self.provider.get_response(prompt)


# Singleton instance 
ai_service = AIService()