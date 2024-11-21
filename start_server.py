from sanic import Request
import json

from excel.webserver.server import app, download_from_url, move_to_google_calendar
from excel.webserver.scheduler.scheduler import scheduler

from telegram.modules import groups
from excel.parser.modules import gcalendar


with open("data.json") as data:
    data_loads = json.load(data)


@app.after_server_start
async def on_start(request: Request) -> None:
    scheduler.start()
    await download_from_url()
    # await move_to_google_calendar()
