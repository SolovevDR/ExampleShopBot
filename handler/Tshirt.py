from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
import config.bot_init

available_tshirt_names = ["красная", "белая", "зеленая", "черная", "синяя"]
available_tshirt_sizes = ["XS", "S", "M", "L", "XL"]


class OrderTshirt(StatesGroup):
    waiting_for_tshirt_name = State()
    waiting_for_tshirt_size = State()

def register_handlers_tshirt(dp: Dispatcher):
    dp.register_message_handler(tshirt_start, commands="tshirt", state="*")
    dp.register_message_handler(tshirt_chosen, state=OrderTshirt.waiting_for_tshirt_name)
    dp.register_message_handler(tshirt_size_chosen, state=OrderTshirt.waiting_for_tshirt_size)

@config.bot_init.dp.callback_query_handler(text_startswith="names_tshirt:")
async def tshirt_call(call: types.CallbackQuery):
    name_tshirt = call.data.split(":")[1]
    print(name_tshirt)
    await call.answer_callback_query(call.id)
    await call.send_message(call.from_user.id, 'Нажата первая кнопка!')

async def tshirt_start(message: types.Message):
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard = types.InlineKeyboardMarkup()
    for name in available_tshirt_names:
        keyboard.add(types.InlineKeyboardButton(
            text=name,
            callback_data=f"names_tshirt:{name}"))
        print(f"names_tshirt:{name}")
    await message.answer("Выберите футболку:", reply_markup=keyboard)
    print('next')
    await OrderTshirt.waiting_for_tshirt_name.set()


# Обратите внимание: есть второй аргумент
async def tshirt_chosen(message: types.Message, state: FSMContext):
    print('tshirt')
    if message.text.lower() not in available_tshirt_names:
        await message.answer("Пожалуйста, выберите футболку, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_tshirt=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for tshirt in available_tshirt_sizes:
        keyboard.add(tshirt)
    # Для простых шагов можно не указывать название состояния, обходясь next()
    await OrderTshirt.next()
    await message.answer("Теперь выберите размер:", reply_markup=keyboard)


async def tshirt_size_chosen(message: types.Message, state: FSMContext):
    if message.text not in available_tshirt_sizes:
        await message.answer("Пожалуйста, выберите размер, используя клавиатуру ниже.")
        return
    user_data = await state.get_data()
    await message.answer(f"Вы заказали {message.text.lower()} футболку {user_data['chosen_tshirt']}.\n"
                         f"Попробуйте теперь заказать напитки: /drinks", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_tshirt(dp: Dispatcher):
    dp.register_message_handler(tshirt_start, commands="tshirt", state="*")
    dp.register_message_handler(tshirt_chosen, state=OrderTshirt.waiting_for_tshirt_name)
    dp.register_message_handler(tshirt_size_chosen, state=OrderTshirt.waiting_for_tshirt_size)


