from django.core.management.base import BaseCommand
from telegram import Bot
from django.utils import timezone
from datetime import date
from dashboard.models import PeopleCounting, Invoice
from django.db.models import Sum, F
import math
import jdatetime
import os
import asyncio
from asgiref.sync import sync_to_async
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
HASH_KEY = "4CbCwLRPAJ5B"

class Command(BaseCommand):
    help = "It sends Telegram reports."

    @sync_to_async
    def getTrafficData(self):
        # now = timezone.now().date() # use the original now in product
        now = date(2025, 9, 1)
        traffic_queryset = PeopleCounting.objects.filter(
            merchant__url_hash=HASH_KEY,
            date=now
            ).values("branch").annotate(
                branch_name=F("branch__name"),
                entry=Sum("entry")
        )
        invoice_queryset = Invoice.objects.filter(
            branch__merchant__url_hash=HASH_KEY,
            date=now
        ).values("branch").annotate(
            branch_name=F("branch__name"),
            total_amount=Sum("total_amount"),
            total_items=Sum("total_items"),
            total_product=Sum("total_product")
        )
        return traffic_queryset, invoice_queryset

    @sync_to_async
    def create_message(self, data: tuple):
        traffic_queryset, invoice_queryset = data
        traffic_queryset_list = list(traffic_queryset)
        invoice_query_list = list(invoice_queryset)
        result = []
        for item_one in traffic_queryset_list:
            dict_item = {}
            for item_two in invoice_query_list:
                if item_one["branch"] == item_two["branch"]:
                    dict_item["branch_name"] = item_one["branch_name"]
                    dict_item["entry"] = item_one["entry"]
                    dict_item["sales"] = item_two["total_amount"]
                    dict_item["invoices"] = item_two["total_items"]
                    dict_item["products"] = item_two["total_product"]
                    try:
                        dict_item["conversion_rate"] = (dict_item["invoices"] / dict_item["entry"]) * 100
                        dict_item["conversion_rate"] = math.floor(dict_item["conversion_rate"])
                    except ZeroDivisionError as e:
                        print(e)
                        dict_item["conversion_rate"] = 0
                    result.append(dict_item)
        
        message_bits = []
        total_traffic = 0
        total_sales = 0
        total_invoices = 0
        total_products = 0
        avg_cv = 0
        total_cv = 0
        loop_index = 0
        persian_date = jdatetime.datetime.now().strftime("%Y/%m/%d، ساعت %H:%M")
        for item in result:
            loop_index += 1
            item["sales"] = item["sales"] / 10
            item["sales"] = int(item["sales"])
            total_traffic += item["entry"]
            total_sales += item["sales"]
            total_invoices += item["invoices"]
            total_products += item["products"]
            total_cv += item['conversion_rate']
            avg_cv = total_cv / loop_index
            avg_cv = math.floor(avg_cv)
            # separators
            item['sales'] = "{:,}".format(item['sales'])
            text = f"{item['branch_name']}\nترافیک: {item['entry']}\tفروش: {item['sales']}\tفاکتور: {item['invoices']}\tکالا: {item['products']}\tنرخ تبدیل: {item['conversion_rate']}"
            message_bits.append(text)
        stats = "\n\n".join(message_bits)
        totals = (
            f"\n\nمجموع ترافیک: {total_traffic}"
            f"\nمجموع فروش: {"{:,}".format(total_sales)}"
            f"\nمجموع فاکتور: {total_invoices}"
            f"\nمجموع کالا: {total_products}"
            f"\nمیانگین نرخ تبدیل: {avg_cv}"
        )
        message = f"{persian_date}\n\n" + stats + totals
        return message
    
    async def send_message(self, chat_id, text, parse_mode, bot):
        await bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._handle_async(*args, **options))

    async def _handle_async(self, *args, **options):
        bot = Bot(token=BOT_TOKEN)

        data = await self.getTrafficData()
        text = await self.create_message(data)
        await self.send_message(CHAT_ID, text, "Markdown", bot)
        self.stdout.write(self.style.SUCCESS("Telegram message successfuly sent"))




            


