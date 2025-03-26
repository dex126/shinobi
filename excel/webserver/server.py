import os
import asyncio
import httpx
import urllib.request
import json

from sanic import Request, Sanic
from sanic import json as json_response
from loguru import logger

from telegram.modules import groups

from excel.webserver import config
from excel.parser.modules import gcalendar
from excel.webserver.scheduler.scheduler import scheduler


semaphore = asyncio.Semaphore(1)


app = Sanic("scheduler_api")
client = httpx.AsyncClient(
    timeout=120,
    limits=httpx.Limits(max_connections=10),
    headers={"User-Agent": "scheduler v1.0"},
)


async def download_from_url() -> None:
    try:
        os.remove("./shinobi.xlsx")
        logger.success("Удален прошлый файл расписания")
        
    except FileNotFoundError:
        logger.debug("Файл расписания не найден")

    try:
        urllib.request.urlretrieve(config.ULTRA_SECRET_URL, "./shinobi.xlsx")
        scheduler.print_jobs()

    except Exception as error:
        logger.error(error)


async def move_to_google_calendar() -> None:
    with open("data.json") as data:
        data_loads = json.load(data)

    for group in groups.get_human_data():
        try:
            await gcalendar.clear_and_fill_calendar(data_loads[group])
            await gcalendar.extract_groups_to_keys() # TODO move to class
            
        except Exception as error:
            logger.error(error)
            continue


@app.post("/start")
async def add_user(request: Request) -> json_response:
    try:
        asyncio.create_task(download_from_url())
        asyncio.create_task(move_to_google_calendar())
        scheduler.start()

        return json_response({"status": "success"}, 200)
    
    except Exception as error:
        logger.error(error)
        return json_response({"status": "failed"}, 500)
