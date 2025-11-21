from .base import AIProvider

class PolicyAdvisor:
    def __init__(self, ai_provider: AIProvider):
        self.ai = ai_provider

    def advise(self, context: str) -> str:
        prompt = f"Given the following context, suggest a backup policy:\n{context}"
        return self.ai.complete(prompt)
