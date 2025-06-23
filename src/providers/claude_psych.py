# src/claude_psych_profile.py
import os
import httpx
import json
from src.core.ai_interface import AIProvider

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

HEADERS = {
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

class ClaudePsychProvider(AIProvider):
    async def analyze(self, profile_data: dict, analysis_type: str) -> str:
        if analysis_type != "psych":
            raise NotImplementedError("Этот провайдер поддерживает только психоанализ")
        prompt = (
            """
Ты — AI-профайлер. На основе профиля VK создай тёплый, точный и виральный AI-портрет человека — его "типаж в соцсетях".

Пиши так, чтобы человек узнал себя, улыбнулся и захотел отправить другу.

📌 Формат markdown с эмодзи:

🔗 Профиль: https://vk.com/{username}

🎭 Ты — [яркое имя типажа]  
(1 строка с живым описанием, например: «Тихий аналитик», «Заряженный мечтатель»)

🧠 AI считает, что ты:
• [эмоциональная особенность или паттерн поведения]  
• [что-то про стиль общения или восприятие людей]  
• [привычка в сети или жизни]  
• [интерес или внутренняя установка]

🎯 Сильная сторона: [что особенно ценно в этом человеке]  
⚠️ Уязвимость: [в чём он может сомневаться, спотыкаться]

🔮 AI-прогноз:
• XX% шанс, что ты [реалистичное + чуть мемное поведение]  
• XX% вероятность, что ты [что-то узнаваемое, бытовое, соцсети]  
• XX% шанс, что ты [шутливо, но правдоподобно]

📊 Уникальность: XX%  
🧬 Энергия в сети: XX/100

💬 Цитата:
> "[короткий девиз — звучит как правда о себе]"

👥 В компании ты — [кто ты среди других, просто и понятно]

🗣️ Хочешь узнать, кто твой друг в соцсетях? Пришли его ссылку сюда.

---

Вот данные профиля VK:
Имя: {name}
Город: {city}
Возраст: {age}
Друзей: {friends_count}
Посты:
{posts}
""".format(
                name=profile_data['name'],
                city=profile_data['city'],
                age=profile_data['age'],
                friends_count=profile_data['friends_count'],
                username=profile_data['username'],
                posts='\n'.join(f'- {post}' for post in profile_data['posts'])
            )
        )
        data = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 700,
            "temperature": 0.7,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(CLAUDE_API_URL, headers=HEADERS, json=data)
            response.raise_for_status()
            return response.json()["content"][0]["text"].strip()

    async def analyze_influencer(self, profile_data: dict) -> str:
        raise NotImplementedError("Анализ блогеров реализован в другом провайдере")

# Для обратной совместимости:
async def generate_report(profile_data: dict) -> str:
    return await ClaudePsychProvider().analyze(profile_data, "psych")