import random
import os
import asyncio
import httpx
from urllib.request import urlretrieve
from datetime import datetime, timedelta

from sanic import Request, Sanic
from sanic import json as json_response
from loguru import logger

from webserver import config
from webserver.scheduler.scheduler import scheduler, CronTrigger


semaphore = asyncio.Semaphore(1)


app = Sanic("scheduler_api")
client = httpx.AsyncClient(
    timeout=120,
    limits=httpx.Limits(max_connections=5),
    headers={"User-Agent": "scheduler v1.0"},
)




async def download_from_url() -> None:
    try:
        os.remove("./shinobi.xlsx")
        logger.success("Удален прошлый файл расписания")
        
    except FileNotFoundError:
        logger.debug("Файл расписания не найден")

    try:
        urlretrieve(config.ULTRA_SECRET_URL, "./shinobi.xlsx")

        current_weekday = datetime.now().weekday()

        for i in range(7-(current_weekday+1)):
            scheduler.add_job(func=download_from_url,
                            trigger="date",
                            run_date=datetime.now() +
                            timedelta(days=i+1),
                            replace_existing=True)
        
        scheduler.print_jobs()

    except Exception as error:
        logger.error(error)


@app.post("/start")
async def add_user(request: Request) -> json_response:
    try:
        asyncio.create_task(download_from_url())

        return json_response({"status": "success"}, 200)
    
    except Exception as error:
        logger.error(error)
        return json_response({"status": "failed"}, 500)
    


async def handle_user(date) -> None:
    async with semaphore:
        try:
            scheduler.add_job(
                func=download_from_url,
                id=datetime.now(),
                trigger="date",
                run_date=datetime.now()
                + timedelta(
                    days=random.randrange(7, 14),
                    hours=random.randrange(1, 9),
                    minutes=random.randrange(1, 59),
                ),
                replace_existing=True,
            )

        except:
            raise
