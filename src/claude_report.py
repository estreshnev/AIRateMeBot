import os
import httpx

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-3-haiku-20240307"
API_URL = "https://api.anthropic.com/v1/messages"

HEADERS = {
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
}

async def generate_report(profile_data: dict) -> str:
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

    async with httpx.AsyncClient(timeout=20) as client:
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
