from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class Merchant(models.Model):
    name = models.CharField(max_length=255)
    rep_first_name = models.CharField(max_length=255)
    rep_last_name = models.CharField(max_length=255)
    rep_mobile_number = models.CharField(max_length=11)
    contract_start_date = models.DateField()
    contract_expiration_date = models.DateField()
    date_created = models.DateTimeField(null=True, default=datetime.now())
    last_modified = models.DateTimeField(auto_now=True)
    
class Country(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(null=True, default=datetime.now())
    last_modified = models.DateTimeField(auto_now=True)

class Province(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country , on_delete=models.CASCADE)
    date_created = models.DateTimeField(null=True, default=datetime.now())
    last_modified = models.DateTimeField(auto_now=True)

class City(models.Model):
    name = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    date_created = models.DateTimeField(null=True, default=datetime.now())
    last_modified = models.DateTimeField(auto_now=True)

class District(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date_created = models.DateTimeField(null=True, default=datetime.now())
    last_modified = models.DateTimeField(auto_now=True)

class Branch(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(null=True, default=datetime.now())
    last_modified = models.DateTimeField(auto_now=True)

class Cam(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    zone = models.CharField(max_length=255)
    entry = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    cam_name = models.CharField(max_length=255)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    google_longitude = models.CharField(max_length=255)
    google_latitude = models.CharField(max_length=255)
    date_created = models.DateTimeField(null=True, default=datetime.now())
    last_modified = models.DateTimeField(auto_now=True)
    
class PeopleCounting(models.Model): # former name: Stats
    date = models.DateField(verbose_name="تاریخ")
    entry = models.IntegerField(default=0, verbose_name="ورودی")
    exit = models.IntegerField(default=0, verbose_name="خروجی")
    cam = models.ForeignKey(Cam, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="شعبه")
    vendor = models.CharField(max_length=255, null=True, verbose_name="فروشگاه")
    date_created = models.DateTimeField(null=True, default=datetime.now())
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "شمارشگر"
        verbose_name_plural = "شمارشگر"

class CampaignCalendar(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام کمپین")
    start_date = models.DateField(verbose_name="تاریخ")
    end_date = models.DateField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    date_created = models.DateTimeField(null=True, default=datetime.now())
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "کمپین"
        verbose_name_plural = "کمپین"

class DefaultDate(models.Model):
    start_date = models.DateField(verbose_name="تاریخ شروع")
    end_date = models.DateField(verbose_name="تاریخ پایان")
    date_created = models.DateTimeField(null=True, default=datetime.now())
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "تاریخ پیش فرض"
        verbose_name_plural = "تاریخ پیش فرض"
