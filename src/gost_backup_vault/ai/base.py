from typing import Protocol, List, Dict

class AIProvider(Protocol):
    def complete(self, prompt: str) -> str: ...
    def chat(self, messages: List[Dict[str, str]]) -> str: ...

class NoopAIProvider(AIProvider):
    def complete(self, prompt: str) -> str:
        return "AI advice not available in NOOP mode."

    def chat(self, messages: List[Dict[str, str]]) -> str:
        return "AI chat not available in NOOP mode."
