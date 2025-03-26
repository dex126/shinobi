
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from excel.webserver import config, server


job_defaults = {
    "coalesce": True,
    "max_instances": 1,
    "misfire_grace_time": None,
    "timezone": config.SCHEDULER_TIMEZONE,
}


scheduler = AsyncIOScheduler()
scheduler.configure(
    job_defaults=job_defaults,
)


@scheduler.scheduled_job('cron', day_of_week="sun")
async def restart_scheduler() -> None:
    await server.download_from_url()
    await server.move_to_google_calendar()
    scheduler.print_jobs()
