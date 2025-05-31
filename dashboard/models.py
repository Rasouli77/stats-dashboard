from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class Merchant(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    rep_first_name = models.CharField(max_length=255, verbose_name="نام نماینده")
    rep_last_name = models.CharField(max_length=255, verbose_name="نام خانوادگی نماینده")
    rep_mobile_number = models.CharField(max_length=11, verbose_name="شماره موبایل نماینده")
    contract_start_date = models.DateField(verbose_name="تاریخ شروع قرارداد")
    contract_expiration_date = models.DateField(verbose_name="تاریخ انقضای قرارداد")
    url_hash = models.CharField(max_length=25, verbose_name="نامک", null=True) # remove null True in Production
    date_created = models.DateTimeField(null=True, default=datetime.now, verbose_name="تاریخ ساخت")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "مرچنت"
        verbose_name_plural = "مرچنت"
    
    
class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    date_created = models.DateTimeField(null=True, default=datetime.now, verbose_name="تاریخ ساخت")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "کشور"
        verbose_name_plural = "کشور"

class Province(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    country = models.ForeignKey(Country , on_delete=models.CASCADE, verbose_name="کشور")
    date_created = models.DateTimeField(null=True, default=datetime.now, verbose_name="تاریخ ساخت")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "استان"
        verbose_name_plural = "استان"

class City(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="استان")
    date_created = models.DateTimeField(null=True, default=datetime.now, verbose_name="تاریخ ساخت")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهر"

class District(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="شهر")
    date_created = models.DateTimeField(null=True, default=datetime.now, verbose_name="تاریخ ساخت")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "منطقه"
        verbose_name_plural = "منطقه"

class Branch(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, verbose_name="مرچنت")
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="منطقه")
    name = models.CharField(max_length=255, verbose_name="نام")
    date_created = models.DateTimeField(null=True, default=datetime.now, verbose_name="تاریخ ساخت")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "شعبه"
        verbose_name_plural = "شعبه"

class Cam(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="کشور")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="استان")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="شهر")
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="منطقه")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="شعبه")
    zone = models.CharField(max_length=255, verbose_name="زون")
    entry = models.CharField(max_length=255, verbose_name="ورودی")
    ip = models.CharField(max_length=255, verbose_name="IP")
    cam_name = models.CharField(max_length=255, verbose_name="نام")
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, verbose_name="مرچنت")
    google_longitude = models.CharField(max_length=255, verbose_name="Google Latitude")
    google_latitude = models.CharField(max_length=255, verbose_name="Google Longitude")
    date_created = models.DateTimeField(null=True, default=datetime.now, verbose_name="تاریخ ساخت")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")

    def __str__(self):
        return f"{self.cam_name} {self.ip}"
    
    class Meta:
        verbose_name = "دوربین"
        verbose_name_plural = "دوربین"
    
class PeopleCounting(models.Model): # former name: Stats
    date = models.DateField(verbose_name="تاریخ")
    entry = models.IntegerField(default=0, verbose_name="ورودی")
    exit = models.IntegerField(default=0, verbose_name="خروجی")
    cam = models.ForeignKey(Cam, on_delete=models.CASCADE, verbose_name="دوربین", related_name="people_counts")
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, verbose_name="مرچنت", related_name="people_counts")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="شعبه", related_name="people_counts")
    date_created = models.DateTimeField(null=True, default=datetime.now, verbose_name="تاریخ ساخت")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")

    def __str__(self):
        return f"{self.merchant.name} {self.branch.name} {self.cam.ip}"

    class Meta:
        verbose_name = "شمارشگر"
        verbose_name_plural = "شمارشگر"

class CampaignCalendar(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام کمپین")
    start_date = models.DateField(verbose_name="تاریخ")
    end_date = models.DateField(verbose_name="تاریخ پایان")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="شعبه")
    date_created = models.DateTimeField(null=True, default=datetime.now, verbose_name="تاریخ ساخت")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "کمپین"
        verbose_name_plural = "کمپین"

class DefaultDate(models.Model):
    user = models.ForeignKey(User, null=True ,on_delete=models.CASCADE, verbose_name="کاربر")
    start_date = models.DateField(verbose_name="تاریخ شروع")
    end_date = models.DateField(verbose_name="تاریخ پایان")
    date_created = models.DateTimeField(null=True, default=datetime.now, verbose_name="تاریخ ساخت")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.start_date} {self.end_date}"

    class Meta:
        verbose_name = "تاریخ پیش فرض"
        verbose_name_plural = "تاریخ پیش فرض"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="کاربر")
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="profile", verbose_name="مرچنت")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        verbose_name = "نمای کاربر"
        verbose_name_plural = "نمای کاربر"
    

