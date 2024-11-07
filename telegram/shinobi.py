import pandas as pd
import dotenv
import logging
import os

from shinobi_bot import config

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils import executor


logging.basicConfig(level=logging.INFO)
dotenv.load_dotenv()

EXCEL_FILE = 'shinobi.xlsx'

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


DAYS_OF_WEEK = {
    "Понедельник": None,
    "Вторник": (8, 13),
    "Среда": (15, 20),
    "Четверг": (22, 27),
    "Пятница": (29, 34),
    "Суббота": (36, 41)
}

# Список индексов кабинетов, соответствующих парам
classroom_indices = {
    3: 4,  # D -> E
    5: 6,  # F -> G
    7: 8,  # H -> I
    9: 10, # J -> K
    11: 12, # L -> M
    13: 14, # N -> O
    15: 16,# P -> Q
    17: 18,# R -> S
    19: 20,# T -> U
    21: 22,# V -> W
    23: 24,# X -> Y
    25: 26,# Z -> AA
    27: 28,# AB -> AC
    29: 30,# AD -> AE
    31: 32,# AF -> AG
    33: 34,# AH -> AI
    35: 36,# AJ -> AK
    37: 38,# AL -> AM
    39: 40,# AN -> AO
    41: 42,# AP -> AQ
    43: 44,# AR -> AS
    45: 46,# AT -> AU
    47: 48,# AV -> AW
    49: 50,# AX -> AY
    51: 52,# AZ -> BA
    53: 54,# BB -> BC
    55: 56,# BD -> BE
    57: 58,# BF -> BG
    59: 60,# BH -> BI
    61: 62,# BJ -> BK
    63: 64,# BL -> BM
    65: 66,# BN -> BO
    67: 68,# BP -> BQ
    69: 70,# BR -> BS
    71: 72,# BT -> BU
    73: 74 # BV -> BW
}


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Проверить расписание")
    markup.add(item)
    await message.answer("Добро пожаловать! Нажмите на кнопку, чтобы проверить расписание.", reply_markup=markup)


@dp.message_handler(lambda message: message.text == "Проверить расписание")
async def select_day(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for day in DAYS_OF_WEEK.keys():
        markup.add(day)
    await message.answer("Выберите день недели:", reply_markup=markup)


@dp.message_handler(lambda message: message.text in DAYS_OF_WEEK)
async def check_schedule(message: types.Message):
    selected_day = message.text
    df = pd.read_excel(EXCEL_FILE, sheet_name=1, header=None)  # Чтение второго листа

    # Проверка выбранного дня
    if selected_day in DAYS_OF_WEEK:
        if DAYS_OF_WEEK[selected_day] is None:
            await message.answer("Этого дня нет в расписании.")
            return
        
        start_row, end_row = DAYS_OF_WEEK[selected_day]
        day_schedule = df.iloc[start_row-1:end_row, [2, 27, 28]]  # Время, Название, Кабинет
        day_schedule.columns = ['Time', 'Subject', 'Classroom']  # Установка имен столбцов

        # Проверяем наличие пар
        if day_schedule.empty or day_schedule['Time'].isnull().all() or day_schedule['Subject'].isnull().all():
            await message.answer(f"Этого дня нет в расписании.")
            return

        # Формируем ответ для группы
        response = f"Расписание на {selected_day}\nДля группы ИСиП-1-9-23:\n\n"
        for idx, row in day_schedule.iterrows():
            time = row['Time'] if pd.notna(row['Time']) else "нет"
            subject = row['Subject'] if pd.notna(row['Subject']) else "нет"
            classroom = row['Classroom'] if pd.notna(row['Classroom']) else "нет"
            response += f"{time}  {subject}  {classroom}\n"

        # Поиск пар БЖ и вывод их только для выбранного дня
        bzh_obzh_schedule = ""
        
        # Получаем все пары на текущий день
        for idx in range(start_row-1, end_row):  # Проходим по строкам текущего дня
            for col in range(3, 75):  # D (3) до BW (74)
                if ("БЖ" in str(df.iloc[idx, col]) or "ОБЖ" in str(df.iloc[idx, col])):
                    # Сравниваем с временем из расписания группы
                    time = df.iloc[idx, 2]  # Получаем время из столбца C
                    classroom_index = col + 1  # Получаем соответствующий кабинет (следующий столбец)
                    if classroom_index < df.shape[1]:
                        classroom = df.iloc[idx, classroom_index] if pd.notna(df.iloc[idx, classroom_index]) else "нет"
                        bzh_obzh_schedule += f"{time}  {df.iloc[idx, col]}  {classroom}\n"

        if bzh_obzh_schedule:
            response +="\nПары БЖ и ОБЖ в данный день:\n" + bzh_obzh_schedule
        else:
            response += "\nПары БЖ и ОБЖ отсутствуют."

        response += "\nСпасибо за терпение!\nУдачного дня😊"
    
    else:
        await message.answer("Этого дня нет в расписании.")
        return

    await message.answer(response)

# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)