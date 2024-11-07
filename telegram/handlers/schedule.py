from aiogram import Router, types, F

from telegram.utils import builder
from telegram.modules import days
from excel.parser import parser


router = Router()

schedule_list = list(days.DAYS_OF_WEEK.keys())


@router.message(F.text == 'Проверить расписание')
async def schedule_handler(message: types.Message):
    get_buttons = builder.schedule_buttons()
    
    await message.answer('<b>⚡️ Выберите день недели:</b>', reply_markup=get_buttons)


@router.message(F.text.in_(schedule_list))
async def schedule_handler(message: types.Message):
    if days.check_day(message.text):
        parsed_info = await parser.do_excel(message.text)

        await message.answer(parsed_info)
    else:
        await message.answer("🎉 <b>Этого дня нет в расписании.</b>")
