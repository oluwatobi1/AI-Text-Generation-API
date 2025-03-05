from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    def get_response(self, prompt):
        """Generate a response based on the given prompt."""
        pass