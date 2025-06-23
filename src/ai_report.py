from openai import AsyncOpenAI
from src.config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

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

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()