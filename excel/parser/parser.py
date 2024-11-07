import pandas as pd
from datetime import datetime

from telegram.modules.days import DAYS_OF_WEEK


EXCEL_FILE = 'shinobi.xlsx'


async def do_excel(selected_day: str) -> str:
    start_time = datetime.now()

    keys = pd.ExcelFile(EXCEL_FILE)
    current_sheet = list(keys.sheet_names)[1]

    df = pd.read_excel(EXCEL_FILE, sheet_name=str(current_sheet), header=None)  # Чтение второго листа
    start_row, end_row = DAYS_OF_WEEK[selected_day]
    day_schedule = df.iloc[start_row-1:end_row, [2, 27, 28]]  # Время, Название, Кабинет
    day_schedule.columns = ['Time', 'Subject', 'Classroom']  # Установка имен столбцов

    # Проверяем наличие пар
    if day_schedule.empty or day_schedule['Time'].isnull().all() or day_schedule['Subject'].isnull().all():
        return("Этого дня нет в расписании.")

    # Формируем ответ для группы
    response = f"<b>Расписание на {selected_day}</b>\nДля группы <code>ИСиП-1-9-23</code>:\n\n"
    for idx, row in day_schedule.iterrows():
        time = row['Time'] if pd.notna(row['Time']) else "нет"
        subject = row['Subject'] if pd.notna(row['Subject']) else "нет"
        classroom = row['Classroom'] if pd.notna(row['Classroom']) else "нет"
        response += f"<u>{time}</u> {subject} <b>{classroom}</b>\n"

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
                    bzh_obzh_schedule += f"<u>{time}</u> {df.iloc[idx, col]} <b>{classroom}</b>\n"

    end_time = datetime.now()

    if bzh_obzh_schedule:
        response += ("\nПары БЖ и ОБЖ в данный день:\n" + bzh_obzh_schedule +
                     "\n\n<code>Ответ получен за {} ms.</code>\n".format(end_time - start_time)+
                     "@shinobi_leave_bot")
    else:
        response += ("\nПары БЖ и ОБЖ отсутствуют.\n\n"
                     "<code>Ответ получен за {} ms.</code>\n".format(end_time - start_time)+
                     "@shinobi_leave_bot")

    return(response)
