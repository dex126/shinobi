'Keyboard Builder' 

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

from telegram.modules import days


def schedule_buttons() -> types.ReplyKeyboardMarkup:
    buttons = days.count_days()

    sch_markup = ReplyKeyboardBuilder()

    for day in buttons:
        sch_markup.button(text=day)

    sch_markup.button(text="Назад")
    sch_markup.adjust(1, 2, 2, 2)

    return sch_markup.as_markup() # TODO inline buttons
