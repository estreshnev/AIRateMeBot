from abc import ABC, abstractmethod
from typing import Dict

class SocialProfileProvider(ABC):
    @abstractmethod
    async def get_profile(self, username: str) -> Dict:
        """Получить профиль пользователя по username"""
        pass

    @abstractmethod
    async def get_group(self, group_id: str) -> Dict:
        """Получить группу по group_id"""
        pass 