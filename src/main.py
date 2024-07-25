import asyncio
import os

from aiogram import Bot, Dispatcher

from handlers.core import router as core_router


async def main() -> None:
    bot = Bot(os.environ['BOT_TOKEN'])
    dp = Dispatcher()
    dp.include_router(core_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
