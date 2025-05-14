from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import call_command
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', hour=16, minute=18)
def daily_task():
    print("Calling management command...")
    call_command("daily_entry_update")

scheduler.start()
