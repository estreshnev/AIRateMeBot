from src.config import MODEL_SOURCE
from src.providers.openai_influencer import OpenAIInfluencerProvider
from src.providers.openai_psych import OpenAIPsychProvider
from src.providers.claude_influencer import ClaudeInfluencerProvider
from src.providers.claude_psych import ClaudePsychProvider

class AIFactory:
    @staticmethod
    def get_provider(analysis_type: str):
        if analysis_type == "influencer":
            if MODEL_SOURCE == "claude":
                return ClaudeInfluencerProvider()
            else:
                return OpenAIInfluencerProvider()
        elif analysis_type == "psych":
            if MODEL_SOURCE == "claude":
                return ClaudePsychProvider()
            else:
                return OpenAIPsychProvider()
        else:
            raise ValueError(f"Неизвестный тип анализа: {analysis_type}") 