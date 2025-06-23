import os
import httpx
from src.core.ai_interface import AIProvider

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-3-haiku-20240307"
API_URL = "https://api.anthropic.com/v1/messages"

HEADERS = {
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
}

class ClaudeInfluencerProvider(AIProvider):
    async def analyze(self, profile_data: dict, analysis_type: str) -> str:
        if analysis_type == "influencer":
            prompt = (
                f"Ты эксперт по digital-маркетингу и социальным медиа. "
                f"Проанализируй профиль пользователя VK как бренд-аналитик и AI-монетизатор.\n\n"
                f"Имя: {profile_data['name']}\n"
                f"Город: {profile_data['city']}\n"
                f"Возраст: {profile_data['age']}\n"
                f"Друзей: {profile_data['friends_count']}\n"
                f"Ссылка: https://vk.com/{profile_data['username']}\n\n"
                f"Посты:\n"
            )
            for post in profile_data["posts"]:
                prompt += f"- {post}\n"
            prompt += (
                "\nОцени:\n"
                "1. Насколько аккаунт живой и вовлечённый\n"
                "2. Как человек раскрывает личность/экспертность\n"
                "3. Есть ли аудитория и вовлечённость\n"
                "4. Дай балл от 0 до 100\n"
                "5. Приблизительный потенциал заработка (в рублях)\n"
                "6. Советы по улучшению: оформление, стиль, подача"
            )
        elif analysis_type == "group_influencer":
            prompt = (
                f"Ты эксперт по digital-маркетингу и социальным медиа. "
                f"Проанализируй сообщество VK как бренд-аналитик и AI-монетизатор.\n\n"
                f"Название: {profile_data['name']}\n"
                f"Описание: {profile_data.get('description', '')}\n"
                f"Участников: {profile_data['members_count']}\n"
                f"Ссылка: https://vk.com/club{profile_data['group_id']}\n\n"
                f"Посты:\n"
            )
            for post in profile_data["posts"]:
                prompt += f"- {post}\n"
            prompt += (
                "\nОцени:\n"
                "1. Насколько группа активна и вовлечённа\n"
                "2. Есть ли аудитория и вовлечённость\n"
                "3. Дай балл от 0 до 100\n"
                "4. Потенциал для рекламы (в рублях)\n"
                "5. Советы по улучшению: оформление, стиль, подача"
            )
        else:
            raise NotImplementedError(f"Этот провайдер не поддерживает analysis_type={analysis_type}")
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                API_URL,
                headers=HEADERS,
                json={
                    "model": MODEL,
                    "max_tokens": 1000,
                    "temperature": 0.7,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
            )
        response.raise_for_status()
        content = response.json()["content"][0]["text"]
        return content.strip()

    async def analyze_psych(self, profile_data: dict) -> str:
        raise NotImplementedError("Психоанализ реализован в другом провайдере")

# Для обратной совместимости:
async def generate_report(profile_data: dict) -> str:
    return await ClaudeInfluencerProvider().analyze(profile_data, "influencer")
