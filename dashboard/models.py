from django.db import models

# Create your models here.
class Stats(models.Model):
    date = models.DateField()
    invoice_count = models.BigIntegerField(default=0, null=True, blank=True)
    invoice_item = models.BigIntegerField(default=0, null=True, blank=True)
    entry = models.IntegerField(default=0)
    branch = models.CharField(max_length=255, null=True)
    vendor = models.CharField(max_length=255, null=True)
