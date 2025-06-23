import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_SOURCE = os.getenv("MODEL_SOURCE", "claude")  # "openai" или "claude"

VK_API_VERSION = os.getenv("VK_API_VERSION", "5.199")
VK_ACCESS_TOKEN = os.getenv("VK_ACCESS_TOKEN", "0")