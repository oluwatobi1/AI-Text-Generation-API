from app.config import Config
from langchain.chat_models import init_chat_model

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def is_local_model():
  return Config.AI_MODEL_PROVIDER not in ["openai", "groq"]

class AIService:
  def __init__(self):
    if is_local_model():
      self.llm = self._get_local_llm()
    else:
      self.model = init_chat_model(Config.AI_MODEL_NAME, model_provider=Config.AI_MODEL_PROVIDER)
  
  def _get_local_llm(self):
    """Get the LLM model based on availability."""
    from langchain.llms import HuggingFacePipeline
    from transformers import pipeline

    # Fallback to a local model (Hugging Face GPT-2)
    local_pipeline = pipeline("text-generation", model="sshleifer/tiny-gpt2")
    return HuggingFacePipeline(pipeline=local_pipeline)
  
  def _get_local_llm_response(self, prompt):
    template = PromptTemplate(input_variables=["prompt"], template="{prompt}")
    chain = LLMChain(llm=self.llm, prompt=template)
    response = chain.run(prompt)
    return response
  

  def get_response(self, prompt):
    if is_local_model():
      return self._get_local_llm_response(prompt)
    return self.model.invoke(prompt).content


# Singleton instance (Created only once)
ai_service = AIService()