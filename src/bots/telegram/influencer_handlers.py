import re
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from src.core.social_factory import SocialProviderFactory
from src.core.ai_factory import AIFactory

influencer_router = Router()

VK_REGEX = re.compile(r"(?:https?://)?vk\.com/([A-Za-z0-9_\.]+)")
VK_GROUP_REGEX = re.compile(r"(?:https?://)?vk\.com/(club|public)([0-9]+)")

@influencer_router.message(F.text.in_(["/start", "/help"]))
async def cmd_start(message: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 Анализировать профиль", callback_data="choose_profile"),
            InlineKeyboardButton(text="👥 Анализировать группу", callback_data="choose_group")
        ]
    ])
    await state.clear()
    await message.answer(
        "Привет! Что будем анализировать?",
        reply_markup=keyboard
    )

@influencer_router.callback_query(F.data == "choose_profile")
async def choose_profile(callback: CallbackQuery, state: FSMContext):
    await state.set_data({"entity_type": "profile"})
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🧠 Психоанализ", callback_data="analyze_psy"),
            InlineKeyboardButton(text="📊 Анализ для рекламы", callback_data="analyze_influencer")
        ]
    ])
    await callback.message.answer(
        "Выбери, какой анализ провести для профиля:",
        reply_markup=keyboard
    )
    await callback.answer()

@influencer_router.callback_query(F.data == "choose_group")
async def choose_group(callback: CallbackQuery, state: FSMContext):
    await state.set_data({"entity_type": "group"})
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Анализ для рекламы", callback_data="analyze_group_influencer")
        ]
    ])
    await callback.message.answer(
        "Выбери, какой анализ провести для группы:",
        reply_markup=keyboard
    )
    await callback.answer()

@influencer_router.callback_query(F.data == "analyze_psy")
async def ask_profile_for_psy(callback: CallbackQuery, state: FSMContext):
    await state.update_data({"analysis_type": "psych"})
    await callback.message.answer("Пришли ссылку на VK-профиль для психоанализа")
    await callback.answer()

@influencer_router.callback_query(F.data == "analyze_influencer")
async def ask_profile_for_influencer(callback: CallbackQuery, state: FSMContext):
    await state.update_data({"analysis_type": "influencer"})
    await callback.message.answer("Пришли ссылку на VK-профиль для анализа рекламы")
    await callback.answer()

@influencer_router.callback_query(F.data == "analyze_group_influencer")
async def ask_group_for_influencer(callback: CallbackQuery, state: FSMContext):
    await state.update_data({"analysis_type": "group_influencer"})
    await callback.message.answer("Пришли ссылку на VK-группу для анализа рекламы")
    await callback.answer()

@influencer_router.message()
async def fallback_handler(message: Message, state: FSMContext):
    user_state = await state.get_data()
    entity_type = user_state.get("entity_type")
    analysis_type = user_state.get("analysis_type")
    if not entity_type or not analysis_type:
        await message.answer("Пожалуйста, выберите, что анализировать, через меню /start ⬇️")
        return
    text = message.text.strip()
    try:
        if entity_type == "profile" and analysis_type:
            await message.answer("🔍 Анализирую VK-профиль…")
            provider, _, entity_id = SocialProviderFactory.get_entity_provider_by_url(text)
            entity = await provider.get_entity(entity_id, "profile")
            ai_provider = AIFactory.get_provider(analysis_type)
            report = await ai_provider.analyze(entity, analysis_type)
            await message.answer(report)
        elif entity_type == "group" and analysis_type == "group_influencer":
            await message.answer("🔍 Анализирую VK-группу…")
            provider, _, entity_id = SocialProviderFactory.get_entity_provider_by_url(text)
            entity = await provider.get_entity(entity_id, "group")
            ai_provider = AIFactory.get_provider("group_influencer")
            report = await ai_provider.analyze(entity, "group_influencer")
            await message.answer(report)
        else:
            await message.answer("Сначала выбери, что анализировать и какой тип анализа через меню /start")
    except Exception as e:
        logging.exception("Ошибка при анализе VK-сущности")
        await message.answer("❌ Произошла ошибка при анализе. Проверь ссылку и попробуй снова через /start. Если ошибка повторяется — попробуй позже или обратись к поддержке.") 