from aiogram import Router, types, F

from telegram.utils import builder
from telegram.handlers.main import send_welcome
from telegram.modules import users

from excel.parser.modules import days
from excel.parser import parser


router = Router()

schedule_list = list(days.DAYS_OF_WEEK.keys())


@router.message(F.text == 'Проверить расписание')
async def schedule_handler(message: types.Message):
    await message.answer('<b>⚡️ Выберите день недели:</b>',
                         reply_markup=builder.schedule_buttons())


@router.message(F.text.in_(schedule_list))
async def day_check(message: types.Message):
    user_data = await users.parse_user_credentials(id=message.from_user.id)

    if user_data[1]:
        if days.check_day(message.text):
            timed_message = await message.answer("Парсим расписание...")

            parsed_info = await parser.do_excel(day=message.text, group=user_data[1])

            await timed_message.edit_text(parsed_info)

            # await message.answer(parsed_info, reply_markup=builder.schedule_buttons())
            
        else:
            await message.answer("🎉 <b>Этого дня нет в расписании.</b>")
    else:
        await send_welcome(message)
