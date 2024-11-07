DAYS_OF_WEEK = {
    "Понедельник": None,
    "Вторник": (8, 13),
    "Среда": (15, 20),
    "Четверг": (22, 27),
    "Пятница": (29, 34),
    "Суббота": (36, 41)
}


def count_days() -> list:
    days_list = []

    for day in DAYS_OF_WEEK.keys():
        days_list.append(day)

    return(days_list)


def check_day(day: str) -> bool:
    if DAYS_OF_WEEK[day] != None:
        return(True)
    else:
        return(False)