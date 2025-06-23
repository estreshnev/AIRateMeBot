# src/handlers.py
import re
import logging
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.config import MODEL_SOURCE
from src.vk_parser import parse_vk_profile

# Динамический импорт генератора отчёта
async def get_generator(analyze_type: str):
    if analyze_type == "psy":
        if MODEL_SOURCE == "claude":
            from src.claude_psych_profile import generate_report
        else:
            from src.psych_profile import generate_report
    else:
        if MODEL_SOURCE == "claude":
            from src.claude_report import generate_report
        else:
            from src.ai_report import generate_report
    return generate_report

router = Router()

VK_REGEX = re.compile(r"(?:https?://)?vk\.com/([A-Za-z0-9_\.]+)")

@router.message(F.text.in_(["/start", "/help"]))
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🧠 Психоанализ", callback_data="analyze_psy"),
            InlineKeyboardButton(text="📊 Оценка бренда", callback_data="analyze_main")
        ]
    ])
    await message.answer(
        "👋 Привет! Я анализирую VK-профили и даю AI-рекомендации.\n\n"
        "Пришли ссылку на VK (например, https://vk.com/id1).",
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith("analyze_"))
async def switch_analysis_mode(callback: CallbackQuery, state: FSMContext):
    analyze_type = callback.data.replace("analyze_", "")
    await state.update_data(analyze_type=analyze_type)
    await callback.answer(f"Тип анализа: {analyze_type}")
    await callback.message.edit_reply_markup()  # убираем кнопки

@router.message()
async def handle_profile(message: Message, state: FSMContext):
    text = message.text.strip()
    vk_match = VK_REGEX.match(text)

    if vk_match:
        username = vk_match.group(1)
        await message.answer("🔍 Анализирую VK-профиль…")

        try:
            profile = await parse_vk_profile(username)
            user_state = await state.get_data()
            analyze_type = user_state.get("analyze_type", "main")
            generate_report = await get_generator(analyze_type)
            report = await generate_report(profile)
            await message.answer(report)
        except Exception as e:
            logging.exception("Ошибка при обработке VK-профиля")
            await message.answer("❌ Не удалось сгенерировать отчёт. Попробуй позже.")
    else:
        await message.answer("🤔 Не понял. Пришли корректную ссылку на VK (например, https://vk.com/id1).")

def register_handlers(dp):
    dp.include_router(router)
