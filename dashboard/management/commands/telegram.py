from django.core.management.base import BaseCommand
from telegram import Bot
from django.utils import timezone
from datetime import date
from dashboard.models import PeopleCounting, Invoice
from django.db.models import Sum, F
import math
import jdatetime

BOT_TOKEN = "8078497152:AAHitT8RjfQ-jaO4gVk_zWjnW5_B_hAOmMs"
CHAT_ID = "-4834300305"
HASH_KEY = "4CbCwLRPAJ5B"

class Command(BaseCommand):
    help = "It sends Telegram reports."
    def handle(self, *args, **options):
        bot = Bot(token=BOT_TOKEN)

        def getTrafficData():
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

        def create_message(data: tuple):
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
        
        def send_message(self):
            data = getTrafficData()
            text = create_message(data)
            bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="Markdown")

        send_message()


# class Command(BaseCommand):
#     help = "It sends Telegram reports."

#     async def send_message(self, bot: Bot, chat_id: str, text: str):
#         """Send the message asynchronously."""
#         await bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")

#     @sync_to_async
#     def get_traffic_data(self):
#         """Fetch traffic data synchronously."""
#         now = date(2025, 9, 1)  # For testing, you can use the original `timezone.now().date()` in production
#         traffic_queryset = PeopleCounting.objects.filter(
#             merchant__url_hash=HASH_KEY,
#             date=now
#         ).values("branch").annotate(
#             branch_name=F("branch__name"),
#             entry=Sum("entry")
#         )
#         return list(traffic_queryset)

#     @sync_to_async
#     def get_invoice_data(self):
#         """Fetch invoice data synchronously."""
#         now = date(2025, 9, 1)  # Same as traffic data
#         invoice_queryset = Invoice.objects.filter(
#             branch__merchant__url_hash=HASH_KEY,
#             date=now
#         ).values("branch").annotate(
#             branch_name=F("branch__name"),
#             total_amount=Sum("total_amount"),
#             total_items=Sum("total_items"),
#             total_product=Sum("total_product")
#         )
#         return list(invoice_queryset)

#     async def create_message(self, data: tuple):
#         """Generate the message text."""
#         traffic_queryset, invoice_queryset = data
#         result = []

#         for item_one in traffic_queryset:
#             dict_item = {}
#             for item_two in invoice_queryset:
#                 if item_one["branch"] == item_two["branch"]:
#                     dict_item["branch_name"] = item_one["branch_name"]
#                     dict_item["entry"] = item_one["entry"]
#                     dict_item["sales"] = item_two["total_amount"]
#                     dict_item["invoices"] = item_two["total_items"]
#                     dict_item["products"] = item_two["total_product"]
#                     try:
#                         dict_item["conversion_rate"] = (dict_item["invoices"] / dict_item["entry"]) * 100
#                         dict_item["conversion_rate"] = math.floor(dict_item["conversion_rate"])
#                     except ZeroDivisionError as e:
#                         print(e)
#                         dict_item["conversion_rate"] = 0
#                     result.append(dict_item)

#         # Prepare the final message
#         message_bits = []
#         total_traffic = 0
#         total_sales = 0
#         total_invoices = 0
#         total_products = 0
#         avg_cv = 0
#         total_cv = 0
#         loop_index = 0
#         persian_date = jdatetime.datetime.now().strftime("%Y/%m/%d، ساعت %H:%M")

#         for item in result:
#             loop_index += 1
#             item["sales"] = item["sales"] / 10
#             item["sales"] = int(item["sales"])
#             total_traffic += item["entry"]
#             total_sales += item["sales"]
#             total_invoices += item["invoices"]
#             total_products += item["products"]
#             total_cv += item['conversion_rate']
#             avg_cv = total_cv / loop_index
#             avg_cv = math.floor(avg_cv)

#             item['sales'] = "{:,}".format(item['sales'])
#             text = f"{item['branch_name']}\nترافیک: {item['entry']}\tفروش: {item['sales']}\tفاکتور: {item['invoices']}\tکالا: {item['products']}\tنرخ تبدیل: {item['conversion_rate']}"
#             message_bits.append(text)

#         stats = "\n\n".join(message_bits)
#         totals = (
#             f"\n\nمجموع ترافیک: {total_traffic}"
#             f"\nمجموع فروش: {"{:,}".format(total_sales)}"
#             f"\nمجموع فاکتور: {total_invoices}"
#             f"\nمجموع کالا: {total_products}"
#             f"\nمیانگین نرخ تبدیل: {avg_cv}"
#         )
#         message = f"{persian_date}\n\n" + stats + totals
#         return message

#     def handle(self, *args, **options):
#         """Main function to fetch data and send message."""
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(self._handle_async(*args, **options))

#     async def _handle_async(self, *args, **options):
#         """Actual async task."""
#         bot = Bot(token=BOT_TOKEN)

#         # Fetch data asynchronously
#         traffic_data = await self.get_traffic_data()
#         invoice_data = await self.get_invoice_data()
        
#         # Create message with fetched data
#         message = await self.create_message((traffic_data, invoice_data))
        
#         # Send the message asynchronously
#         await self.send_message(bot, CHAT_ID, message)

#         # Success message
#         self.stdout.write(self.style.SUCCESS("Bot message sent successfully!"))


            


