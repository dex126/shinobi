from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from loguru import logger

from telegram import config
from telegram.utils import db


bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=RedisStorage(db.states_db))



async def bot_entrypoint() -> None:
    from telegram.handlers import main, schedule, groups, academic_hours

    dp.include_routers(
        main.router,
        schedule.router,
        groups.router,
        academic_hours.router,
    )

    logger.debug("Бот запущен.")
    
    await dp.start_polling(bot)
