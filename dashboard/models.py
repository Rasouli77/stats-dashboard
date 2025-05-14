from django.db import models

# Create your models here.
class Stats(models.Model):
    date = models.DateField(verbose_name="تاریخ")
    invoice_count = models.BigIntegerField(default=0, null=True, blank=True, verbose_name="تعداد فاکتور")
    invoice_item = models.BigIntegerField(default=0, null=True, blank=True, verbose_name="آیتم فاکتور")
    entry = models.IntegerField(default=0, verbose_name="ورودی")
    branch = models.CharField(max_length=255, null=True, verbose_name="شعبه")
    vendor = models.CharField(max_length=255, null=True, verbose_name="فروشگاه")

    class Meta:
        verbose_name = "شمارشگر"
        verbose_name_plural = "شمارشگر"