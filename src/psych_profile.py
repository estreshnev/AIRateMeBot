# src/psych_profile.py
from openai import AsyncOpenAI
from src.config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def generate_report(profile_data: dict) -> str:
    prompt = (
        f"Ты психолог и специалист по поведенческому анализу. На основе данных VK-профиля оцени:\n\n"
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
        "\nСделай краткий психологический анализ личности по постам. Укажи:\n"
        "1. Чем может интересоваться человек (по содержанию)\n"
        "2. Какая у него жизненная позиция или настроение\n"
        "3. Чем, возможно, он занимается или работает\n"
        "4. Какие темы ему потенциально интересны\n"
        "5. Забавный факт о нём с вероятностью (например: 65% он интроверт)\n"
        "6. Дай гипотетическую оценку по известным типологиям:\n"
        "   - MBTI (например, INTP, ENFJ)\n"
        "   - Big Five (по шкале 0–100 для каждого фактора)\n"
        "   - Тёмная триада (по желанию, кратко)\n"
        "\nБудь кратким, дружелюбным, добавь эмодзи."
    )

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700,
        temperature=0.8,
    )

    return response.choices[0].message.content.strip()
