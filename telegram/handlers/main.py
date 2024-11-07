"Приветственное сообщение"

from aiogram import Router, filters, types, F
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(filters.Command(commands='start'))
async def send_welcome(message: types.Message, state: FSMContext):
    await state.clear()

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text='Проверить расписание'),
            ],
        ], resize_keyboard=True,
    )

    await message.answer(f"<b>Добро пожаловать, {message.from_user.first_name}</b>\n\n"
                         "<i>Нажмите на кнопку, чтобы проверить расписание.</i>",
                         reply_markup=keyboard) # TODO Bot Logo


@router.message(F.text == 'Назад')
async def schedule_handler(message: types.Message, state: FSMContext):
    await send_welcome(message, state)
