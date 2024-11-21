from datetime import datetime, date

from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from loguru import logger

from excel.parser.modules import days
from excel.parser import parser
from telegram.modules import groups


calendar = GoogleCalendar(credentials_path="credentials.json")

today = date.today()
weekday = today.isoweekday()
current_monday = today.day - today.weekday()


DAYS = {"Понедельник": current_monday,
        "Вторник": current_monday+1,
        "Среда": current_monday+2,
        "Четверг": current_monday+3,
        "Пятница": current_monday+4,
        "Суббота": current_monday+5}


async def add_subject_to_calendar(subject: dict) -> None:
    time = datetime.now()
    time_of_school = str(subject["time"]).split(":")
    if subject["subject"] != "нет":
        event = Event(
            subject["subject"],
            start=datetime(time.year, time.month, DAYS[subject["day_of_week"]],
                           int(time_of_school[0]), int(time_of_school[1])),

            description=subject["classroom"],
        )

        calendar.add_event(event=event, calendar_id=subject["group_id"])

    return


async def parse_all(group: str) -> bool:
    for key in DAYS.keys():
            if days.check_day(key):
                await parser.do_excel(day=key, group=group, all=True)

    return(True)


async def extract_groups_to_keys() -> None:
    for group in groups.get_human_data():
        await parse_all(group)

    return


async def clear_and_fill_calendar(group_id: str) -> None:
    time = datetime.now()

    for event in calendar.get_events(time_min=datetime(time.year, time.month, DAYS["Понедельник"]),
                                     calendar_id=group_id):
            
            calendar.delete_event(event, calendar_id=group_id)

    return
