import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from src.core.social_factory import SocialProviderFactory
from src.core.ai_factory import AIFactory

influencer_router = Router()

@influencer_router.message(F.text.in_(["/start", "/help"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_data({"entity_type": "profile", "analysis_type": "psych"})
    await message.answer("Пожалуйста, пришли ссылку на VK-профиль для психоанализа (например, https://vk.com/id1)")

@influencer_router.message()
async def fallback_handler(message: Message, state: FSMContext):
    user_state = await state.get_data()
    entity_type = user_state.get("entity_type")
    analysis_type = user_state.get("analysis_type")
    if entity_type != "profile" or analysis_type != "psych":
        await message.answer("Пожалуйста, пришли ссылку на VK-профиль для психоанализа через /start")
        return
    text = message.text.strip()
    try:
        await message.answer("🔍 Анализирую VK-профиль…")
        provider, _, entity_id = SocialProviderFactory.get_entity_provider_by_url(text)
        entity = await provider.get_entity(entity_id, "profile")
        ai_provider = AIFactory.get_provider("psych")
        report = await ai_provider.analyze(entity, "psych")
        await message.answer(report, parse_mode='Markdown')
    except Exception as e:
        logging.exception("Ошибка при психоанализе VK-профиля")
        await message.answer("❌ Произошла ошибка при анализе. Проверь ссылку и попробуй снова через /start. Если ошибка повторяется — попробуй позже или обратись к поддержке.") 