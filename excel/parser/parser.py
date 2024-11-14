import re
import pandas as pd
import requests
from datetime import datetime

from excel import config
from excel.parser.modules.days import DAYS_OF_WEEK


async def do_excel(day: str, group: str) -> str: # эта функция приговорена к полному рефакторингу (она говно)
    """
    Парсер расписания из таблицы Excel.
    Требует день недели и группу юзера.
    Возвращает готовое расписание.
    """

    start_time = datetime.now() # таймер
    
    parsed_group = requests.get(f"http://{config.API_HOST}/groups/"+group).json()

    keys = pd.ExcelFile('shinobi.xlsx')
    current_sheet = keys.sheet_names[len(keys.sheet_names)-1]

    df = pd.read_excel(keys, sheet_name=current_sheet, header=None)

    start_row, end_row = DAYS_OF_WEEK[day]
    day_schedule = df.iloc[start_row-1:end_row,
                           list(map(int, re.findall(r'\d+',parsed_group["list"])))]

    day_schedule.columns = ['Time', 'Subject', 'Classroom']

    response = (f"<b>Расписание на {day}</b> "
                f"[<code>{group}</code>]:\n"
                f"[<code>{current_sheet}</code>]\n\n")

    for idx, row in day_schedule.iterrows():
        try:
            time = datetime.strptime(str(row['Time']), '%H:%M:%S').strftime('%H:%M') \
                   if pd.notna(row['Time']) else "нет"
            
        except ValueError:
            escaped_time = "0"+str(row['Time']).replace(' ', '')
            time = escaped_time \
                   if pd.notna(row['Time']) else "нет"

        subject = row['Subject'] if pd.notna(row['Subject']) else "нет"
        classroom = row['Classroom'] if pd.notna(row['Classroom']) else "нет"

        response += f"<u>{time}</u> {subject} [<b>{classroom}</b>]\n"

    bzh_obzh_schedule = ""
    
    for idx in range(start_row-1, end_row):
        for col in range(3, 75):
            if ("БЖ" in str(df.iloc[idx, col]) or "ОБЖ" in str(df.iloc[idx, col])):
                time = df.iloc[idx, 2]
                classroom_index = col + 1
                if classroom_index < df.shape[1]:
                    classroom = df.iloc[idx, classroom_index] \
                        if pd.notna(df.iloc[idx, classroom_index]) else "нет"
                    
                    bzh_obzh_schedule += f"<u>{time}</u> {df.iloc[idx, col]} <b>{classroom}</b>\n"

    end_time = datetime.now()

    if group == "ИСиП-1-9-23":
        if bzh_obzh_schedule:
            response += ("\nПары БЖ и ОБЖ в данный день:\n" + bzh_obzh_schedule)
            
        else:
            response += ("\nПары БЖ и ОБЖ отсутствуют.")
            
    response += ("\n<code>Ответ получен за {} ms.</code>\n".format(end_time - start_time)+
                 "@shinobi_leave_bot")

    return(response)
