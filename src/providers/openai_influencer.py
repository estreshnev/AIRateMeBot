from openai import AsyncOpenAI
from src.config import OPENAI_API_KEY
from src.core.ai_interface import AIProvider

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

class OpenAIInfluencerProvider(AIProvider):
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
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    async def analyze_psych(self, profile_data: dict) -> str:
        raise NotImplementedError("Психоанализ реализован в другом провайдере")

# Для обратной совместимости:
async def generate_report(profile_data: dict) -> str:
    return await OpenAIInfluencerProvider().analyze(profile_data, "influencer")