# AIRateMeBot

AI-бот для анализа профилей соцсетей (VK, Telegram и др.) с помощью ИИ (Claude, OpenAI и др.)

## 🚀 Быстрый старт

1. Установи зависимости:

```bash
pip install -r requirements.txt
```

2. Создай `.env` файл:

```env
TELEGRAM_TOKEN=твой_токен_бота
OPENAI_API_KEY=ключ_от_openai
ANTHROPIC_API_KEY=ключ_от_claude
VK_SERVICE_KEY=vk_service_key
MODEL_SOURCE=openai  # или claude
```

3. Запусти:

```bash
python main.py
```

## 🧩 Структура проекта

```
src/
  core/
    ai_interface.py         # Абстракция для AI-провайдеров
    profile_analyzer.py     # Бизнес-логика анализа профиля
    entities.py             # Общие сущности: Profile, Group и т.д.
  bots/
    telegram/
      bot.py
      handlers.py
    vk_miniapps/
      bot.py
      handlers.py
  providers/
    claude.py
    openai.py
    # ...
  social/
    vk.py
    telegram.py
    # ...
  config.py
main.py
requirements.txt
README.md
```

## 🛠 Возможности

* Поддержка нескольких платформ: Telegram, VK Mini Apps
* Поддержка нескольких AI: OpenAI, Claude
* Анализ профилей и групп VK
* FSM хранение типа анализа на пользователя

## 🔮 В планах

* Поддержка Instagram, других соцсетей
* PDF-отчёты и шаринг ссылкой
* Оплата за анализ / подписка
* Интерфейс для агентств и брендов

---

👤 MVP для теста гипотезы «Сколько ты стоишь в соцсетях»
