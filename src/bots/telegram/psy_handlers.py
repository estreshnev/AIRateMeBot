import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

psy_router = Router()
# Здесь больше нет обработчиков сообщений — вся логика через fallback в influencer_handlers.py 