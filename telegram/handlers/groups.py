from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from telegram.handlers import main
from telegram.states.new_group import NewGroup
from telegram.modules import groups, users
from telegram.utils import builder


router = Router()


@router.message(NewGroup.waiting_for_group)
async def receive_user_group(message: types.Message, state: FSMContext):
    groups_list = groups.get_human_data()

    user_data = await users.parse_user_credentials(id=message.from_user.id)
   
    if message.text in groups_list:
        await users.add_user(id=message.from_user.id,
                             is_pinned=user_data[0],
                             group=message.text)
        
        await message.answer(f"⚡️ <b>Выбрана группа {message.text}</b>")
        await main.send_welcome(message, state)

    else:
        await message.answer("Я не нашёл такой группы в списке. 😓",
                             reply_markup=builder.group_buttons())
