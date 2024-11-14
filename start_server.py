from sanic import Request

from excel.webserver.server import app, download_from_url
from excel.webserver.scheduler.scheduler import scheduler


@app.after_server_start
async def on_start(request: Request) -> None:
    scheduler.start()
    await download_from_url()
