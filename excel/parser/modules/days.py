"""Модуль для работы с днями недели и их ячейками."""

import pandas


DAYS_OF_WEEK = {
    "Понедельник": None,
    "Вторник": (8, 13),
    "Среда": (15, 20),
    "Четверг": (22, 27),
    "Пятница": (29, 34),
    "Суббота": (36, 41)
}


def count_days() -> list:
    """
    Переводит словарь дней недели в список.
    """

    days_list = []

    for day in DAYS_OF_WEEK.keys():
        days_list.append(day)

    return(days_list)


def check_day(day: str) -> bool:
    """
    Проверяет наличие Понедельника в расписании и корректирует словарь.
    """
    
    keys = pandas.ExcelFile('shinobi.xlsx')
    current_sheet = keys.sheet_names[len(keys.sheet_names)-1]

    df = pandas.read_excel('shinobi.xlsx', sheet_name=current_sheet, usecols='A')

    if "Понедельник" in str(df):
        DAYS_OF_WEEK["Понедельник"] = (8, 15)
        DAYS_OF_WEEK["Вторник"] = (17, 22)
        DAYS_OF_WEEK["Среда"] = (24, 29)
        DAYS_OF_WEEK["Четверг"] = (31, 36)
        DAYS_OF_WEEK["Пятница"] = (38, 43)
        DAYS_OF_WEEK["Суббота"] = (45, 50)
    else:
        DAYS_OF_WEEK["Понедельник"] = None
        DAYS_OF_WEEK["Вторник"] = (8, 13)
        DAYS_OF_WEEK["Среда"] = (15, 20)
        DAYS_OF_WEEK["Четверг"] = (22, 27)
        DAYS_OF_WEEK["Пятница"] = (29, 34)
        DAYS_OF_WEEK["Суббота"] = (36, 41)

    if DAYS_OF_WEEK[day] != None:
        return(True)
    else:
        return(False)
