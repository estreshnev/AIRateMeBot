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
            f"""
Ты — AI-профайлер. На основе публичного профиля VK создай виральный, тёплый и узнаваемый психотип.  
Формат — markdown с эмодзи, стиль — “AI как гороскоп, но умный”. Максимум 3500 символов.

---

🔗 Профиль: https://vk.com/{profile_data['username']}

🎭 **AI-типаж:** [Название + 1 строка описания]

🧠 **Характер:**
• [поведенческая черта]  
• [эмоциональный паттерн]  
• [цифровая привычка]

🎯 **Сила:** [что тебя выделяет]  
⚠️ **Уязвимость:** [что мешает или тормозит]

🔮 **Прогнозы:**
• XX% ты [действие]  
• XX% ты [черта или факт]  
• XX% совпадение с типажом “[AI-тип]”

📊 Уникальность: XX%  
Энергия в сети: XX/100

💬 Цитата:
> "[фраза, описывающая тебя]"

🪐 **AI-Натальная карта:**
• Знак влияния — [например, Луна в Водолее]  
• Планета силы — [Меркурий, Венера и т.д.]  
• Предсказание — "[одна строка, персональная]"

👥 Хочешь узнать, кто твой друг в соцсетях? Просто пришли его ссылку сюда.

---

Вот данные профиля VK:
Имя: {profile_data['name']}
Город: {profile_data['city']}
Возраст: {profile_data['age']}
Друзей: {profile_data['friends_count']}
Посты:
{chr(10).join(f'- {post}' for post in profile_data['posts'])}
"""
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