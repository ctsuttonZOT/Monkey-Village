import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_API_SECRET = os.getenv("BOT_TOKEN")