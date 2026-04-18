import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import get_router

# Bot configuration
BOT_TOKEN = "7588478024:AAHUd6_2ntEUmVOvl5UGtnAe8wnB8WDdjD0"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main function to start the bot"""
    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Register handlers
    router = get_router(bot)
    dp.include_router(router)

    logger.info("Starting DeadBoot bot...")

    # Start polling
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
