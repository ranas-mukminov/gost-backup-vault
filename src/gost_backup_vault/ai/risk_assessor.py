from .base import AIProvider

class RiskAssessor:
    def __init__(self, ai_provider: AIProvider):
        self.ai = ai_provider

    def assess(self, answers: dict[str, str]) -> str:
        prompt = "Assess the backup risks based on these answers:\n"
        for k, v in answers.items():
            prompt += f"- {k}: {v}\n"
        return self.ai.complete(prompt)
