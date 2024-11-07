from sanic import Request, Sanic

from webserver.server import app
from webserver.scheduler.scheduler import scheduler


@app.after_server_start
async def on_start(request: Request) -> None:
    scheduler.start()
    scheduler.print_jobs()
