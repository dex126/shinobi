'Keyboard Builder' 

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

from excel.parser.modules import days
from telegram.modules import groups


def menu_buttons(data: str | None) -> types.ReplyKeyboardMarkup:
    if data == None:
        data = "Нет"

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text='Проверить расписание'),
            ],
            [
                types.KeyboardButton(text=f'Сменить группу [{data}]'),
            ],
            [
                types.KeyboardButton(text='Расписание звонков'),
            ]
        ], resize_keyboard=True,
    )

    return keyboard


def schedule_buttons() -> types.ReplyKeyboardMarkup:
    buttons = days.count_days()

    sch_markup = ReplyKeyboardBuilder()

    for day in buttons:
        sch_markup.button(text=day)

    sch_markup.button(text="Назад")
    sch_markup.adjust(1, 2, 2, 2)

    return sch_markup.as_markup() # TODO inline buttons


def group_buttons() -> types.ReplyKeyboardMarkup:
    buttons = groups.get_human_data()

    grp_markup = ReplyKeyboardBuilder()

    for group in buttons:
        grp_markup.button(text=group)

    grp_markup.button(text='Назад')
    grp_markup.adjust(3)

    return grp_markup.as_markup() # TODO inline buttons with carousel


def url_button(link: str) -> types.InlineKeyboardMarkup:
    URL = types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text='🔗 Гугл календарь',
                                                     url=link)]]
        )
    
    return URL
