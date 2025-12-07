import asyncio
from bot.core import run_bot

if __name__ == "__main__":
    try:
        print("🚀 Bot starting...")
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("Bot stopped manually.")
