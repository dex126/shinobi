"Приветственное сообщение"

from aiogram import Router, filters, types, F
from aiogram.fsm.context import FSMContext

from telegram.modules import users, groups
from telegram.states.new_group import NewGroup
from telegram.utils import builder

router = Router()


@router.message(filters.Command(commands='start'))
async def send_welcome(message: types.Message, state: FSMContext):
    await state.clear()

    user_data = await users.parse_user_credentials(id=message.from_user.id)

    if user_data[1] not in groups.get_human_data():
        await message.answer("⚡️ <b>Пожалуйста, выберите вашу группу:</b>",
                             reply_markup=builder.group_buttons())
        
        await state.set_state(NewGroup.waiting_for_group)

    else:
        await message.answer(f"<b>Добро пожаловать, {message.from_user.first_name}</b>\n\n"
                            "<i>Нажмите на кнопку, чтобы проверить расписание.</i>",
                            reply_markup=builder.menu_buttons(data=user_data[1])) # TODO Bot Logo
        

@router.message(F.text.startswith('Сменить группу'))
async def change_group(message: types.Message, state: FSMContext):
    await message.answer("⚡️ <b>Пожалуйста, выберите вашу группу:</b>",
                             reply_markup=builder.group_buttons())
    
    await state.set_state(NewGroup.waiting_for_group) # мне не поебать (dex)


@router.message(F.text == 'Назад')
async def back(message: types.Message, state: FSMContext):
    await send_welcome(message, state)
