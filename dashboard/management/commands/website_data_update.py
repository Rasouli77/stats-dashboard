from dashboard.models import WebsiteSales, WebsiteVisit, Merchant
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from ...matomo import get_matomo_daily
from dotenv import load_dotenv
import logging
import subprocess
import os
logger = logging.getLogger(__name__)

load_dotenv()

MATOMO_API_TOKEN = os.environ.get("MATOMO_API_TOKEN")
MATOMO_URL = "https://matomo.webpoosh.org"
ID_SITE = 1

# Use the variables below for the date range
start = "2025-10-01"
end = "2025-12-01"

# Use this for cron jobs
today = timezone.now().date()
today_str = today.strftime("%Y-%m-%d")

# Merchant
merchant = Merchant.objects.get(pk=1)

class Command(BaseCommand):
    help = "run updates for website data"
    def handle(self, *args, **kwargs):
        matomo_data_dictionary = get_matomo_daily(MATOMO_URL, MATOMO_API_TOKEN, ID_SITE, "2025-10-01", "2025-12-06")
        print(matomo_data_dictionary)
        for key, value in matomo_data_dictionary.items():
            WebsiteVisit.objects.update_or_create(
                merchant=merchant,
                date = key,
                defaults = {
                    'unique_visitors': int(value['nb_uniq_visitors']) if value != [] else 0,
                    'visits': int(value['nb_visits']) if value != [] else 0,
                    'bounce_rate': int(str(value['bounce_rate'])[:2]) if value != [] else 0,
                    'actions_count': int(value['nb_actions']) if value != [] else 0,
                    'sum_time_spent': int(value['sum_visit_length']) if value != [] else 0,
                    'avg_time_spent': int(value['avg_time_on_site']) if value != [] else 0,
                    'actions_per_visit': float(value['nb_actions_per_visit']) if value != [] else 0
                }
            )
            print('successfully created')


# '2025-11-01': {'nb_uniq_visitors': 4174, 'nb_users': 0, 'nb_visits': 4984, 'nb_actions': 18619, 'nb_visits_converted': 40, 'bounce_count': 2213, 'sum_visit_length': 1034688, 'max_actions': 175, 'bounce_rate': '44%', 'nb_actions_per_visit': 3.7, 'avg_time_on_site': 208}