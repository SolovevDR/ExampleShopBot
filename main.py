import asyncio
import config.bot_init

from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage



async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/tshirt", description="Заказать блюда"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.bot_init.BOT_TOKEN)
    config.bot_init.dp = Dispatcher(bot, storage=MemoryStorage())

    dp = config.bot_init.dp
    print(config.bot_init.dp)

    from handler.Tshirt import register_handlers_tshirt
    from handler.common import register_handlers_common

    # Регистрация хэндлеров
    register_handlers_common(dp)
    # register_handlers_drinks(dp)
    register_handlers_tshirt(dp)



    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
