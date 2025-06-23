from abc import ABC, abstractmethod
from typing import Dict

class AIProvider(ABC):
    @abstractmethod
    async def analyze(self, profile_data: Dict, analysis_type: str) -> str:
        """
        Универсальный анализ профиля или группы.
        analysis_type может быть:
        - 'influencer' — анализ профиля для рекламы
        - 'psych' — психоанализ профиля
        - 'group_influencer' — анализ группы для рекламы
        - 'group_psych' — психоанализ группы
        и т.д.
        """
        pass 