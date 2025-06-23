# AIRateMeBot

AI-бот в Telegram, который анализирует VK-профили и выдаёт отчёты:

* 📊 Бренд-анализ (вовлечённость, советы по монетизации)
* 🧠 Психоанализ (MBTI, интересы, Big Five, с эмодзи)

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

## 🛠 Возможности

* Поддержка двух моделей: `openai`, `claude`
* Переключение анализа через inline-кнопки: `бренд` / `психо`
* Парсинг профиля и последних постов через VK API
* FSM хранение типа анализа на пользователя

## 🧩 Структура проекта

```
├── main.py
├── requirements.txt
├── .env
└── src/
    ├── handlers.py
    ├── config.py
    ├── vk_parser.py
    ├── ai_report.py
    ├── claude_report.py
    ├── psych_profile.py
    └── claude_psych_profile.py
```

## 🔮 В планах

* Поддержка Telegram и Instagram
* PDF-отчёты и шаринг ссылкой
* Оплата за анализ / подписка
* Интерфейс для агентств и брендов

---

👤 Сделано для теста гипотезы «Сколько ты стоишь в соцсетях» — MVP за 2 недели
