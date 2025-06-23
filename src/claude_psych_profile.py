# src/claude_psych_profile.py
import os
import httpx
import json

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

HEADERS = {
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

async def generate_report(profile_data: dict) -> str:
    prompt = (
        f"Ты опытный психолог и специалист по профайлингу. Проанализируй VK-профиль и выдай краткий, дружелюбный психологический портрет.\n\n"
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
        "\nСделай гипотетическую оценку по:\n"
        "1. Интересам\n"
        "2. Настроению и жизненной позиции\n"
        "3. Возможной профессии\n"
        "4. Темам, которые могут его заинтересовать\n"
        "5. Забавный факт с вероятностью (например: 70% интроверт)\n"
        "6. MBTI\n"
        "7. Big Five (0–100 по каждому параметру)\n"
        "8. При желании — кратко по тёмной триаде\n\n"
        "Добавь эмодзи. Будь лаконичным и человечным."
    )

    data = {
        "model": "claude-3-opus-20240229",
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