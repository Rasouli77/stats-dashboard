from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Merchant(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    rep_first_name = models.CharField(max_length=255, verbose_name="نام نماینده")
    rep_last_name = models.CharField(
        max_length=255, verbose_name="نام خانوادگی نماینده"
    )
    rep_mobile_number = models.CharField(
        max_length=11, verbose_name="شماره موبایل نماینده"
    )
    contract_start_date = models.DateField(verbose_name="تاریخ شروع قرارداد")
    contract_expiration_date = models.DateField(verbose_name="تاریخ انقضای قرارداد")
    url_hash = models.CharField(
        max_length=25, verbose_name="نامک", null=True, db_index=True, unique=True
    )  # remove null True in Production
    date_created = models.DateTimeField(
        null=True, default=datetime.now, verbose_name="تاریخ ساخت"
    )
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین تغییر"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "مرچنت"
        verbose_name_plural = "مرچنت"


class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    date_created = models.DateTimeField(
        null=True, default=datetime.now, verbose_name="تاریخ ساخت"
    )
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین تغییر"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "کشور"
        verbose_name_plural = "کشور"


class Province(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="کشور")
    date_created = models.DateTimeField(
        null=True, default=datetime.now, verbose_name="تاریخ ساخت"
    )
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین تغییر"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "استان"
        verbose_name_plural = "استان"


class City(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, verbose_name="استان"
    )
    date_created = models.DateTimeField(
        null=True, default=datetime.now, verbose_name="تاریخ ساخت"
    )
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین تغییر"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهر"


class District(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="شهر")
    date_created = models.DateTimeField(
        null=True, default=datetime.now, verbose_name="تاریخ ساخت"
    )
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین تغییر"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "منطقه"
        verbose_name_plural = "منطقه"


class Branch(models.Model):
    merchant = models.ForeignKey(
        Merchant, on_delete=models.CASCADE, verbose_name="مرچنت", db_index=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name="کشور", null=True, blank=True
    )
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, verbose_name="استان", null=True, blank=True
    )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name="شهر", null=True, blank=True
    )
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, verbose_name="منطقه", null=True, blank=True
    )
    name = models.CharField(max_length=255, verbose_name="نام", db_index=True)
    date_created = models.DateTimeField(
        null=True, default=datetime.now, verbose_name="تاریخ ساخت"
    )
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین تغییر"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "شعبه"
        verbose_name_plural = "شعبه"


class Cam(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="کشور")
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, verbose_name="استان"
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="شهر")
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, verbose_name="منطقه"
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="شعبه")
    zone = models.CharField(max_length=255, verbose_name="زون")
    entry = models.CharField(max_length=255, verbose_name="ورودی")
    ip = models.CharField(max_length=255, verbose_name="IP")
    cam_name = models.CharField(max_length=255, verbose_name="نام")
    merchant = models.ForeignKey(
        Merchant, on_delete=models.CASCADE, verbose_name="مرچنت"
    )
    google_longitude = models.CharField(max_length=255, verbose_name="Google Latitude")
    google_latitude = models.CharField(max_length=255, verbose_name="Google Longitude")
    date_created = models.DateTimeField(
        null=True, default=datetime.now, verbose_name="تاریخ ساخت"
    )
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین تغییر"
    )
    status = models.BooleanField(null=True, verbose_name="وضعیت", blank=True)

    def __str__(self):
        return f"{self.cam_name} {self.ip}"

    class Meta:
        verbose_name = "دوربین"
        verbose_name_plural = "دوربین"


class PeopleCounting(models.Model):
    date = models.DateField(verbose_name="تاریخ", db_index=True)
    entry = models.IntegerField(default=0, verbose_name="ورودی")
    exit = models.IntegerField(default=0, verbose_name="خروجی")
    cam = models.ForeignKey(
        Cam,
        on_delete=models.CASCADE,
        verbose_name="دوربین",
        related_name="people_counts",
    )
    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        verbose_name="مرچنت",
        related_name="people_counts",
        db_index=True,
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name="شعبه",
        related_name="people_counts",
        db_index=True,
    )
    date_created = models.DateTimeField(
        null=True, default=datetime.now, verbose_name="تاریخ ساخت"
    )
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین تغییر"
    )

    def __str__(self):
        return f"{self.merchant.name} {self.branch.name} {self.cam.ip}"

    class Meta:
        verbose_name = "شمارشگر"
        verbose_name_plural = "شمارشگر"
        indexes = [models.Index(fields=["merchant", "date"])]


class Campaign(models.Model):
    campaign_types = [("ویترین", "ویترین"), ("فروش", "فروش")]
    group_id = models.CharField(max_length=36, null=True, blank=True, db_index=True)
    name = models.CharField(max_length=255, verbose_name="نام کمپین")
    start_date = models.DateField(verbose_name="تاریخ", db_index=True)
    end_date = models.DateField(
        verbose_name="تاریخ پایان", null=True, blank=True, db_index=True
    )
    campaign_type = models.CharField(
        choices=campaign_types,
        null=True,
        blank=True,
        max_length=10,
        verbose_name="نوع کمپین",
    )
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, verbose_name="شعبه", db_index=True
    )
    cost = models.CharField(max_length=255, verbose_name="هزینه", null=True, blank=True)
    date_created = models.DateTimeField(
        null=True, default=datetime.now, verbose_name="تاریخ ساخت"
    )
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین تغییر"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "کمپین"
        verbose_name_plural = "کمپین"
        indexes = [models.Index(fields=["branch", "start_date", "end_date"])]


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="کاربر",
        db_index=True,
    )
    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="مرچنت",
        db_index=True,
    )
    mobile = models.CharField(
        max_length=11, verbose_name="شماره تلفن", null=True, blank=True
    )
    is_manager = models.BooleanField(default=False, verbose_name="مدیر", db_index=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "نمای کاربر"
        verbose_name_plural = "نمای کاربر"


class PermissionToViewBranch(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="permissiontoviewbranch",
        verbose_name="کاربر",
        db_index=True,
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="permissiontoviewbranch",
        verbose_name="شعبه",
        db_index=True,
    )
    date_created = models.DateTimeField(
        null=True, default=datetime.now, verbose_name="تاریخ ساخت"
    )
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین تغییر"
    )

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "مجوز شعبه"
        verbose_name_plural = "مجوز شعبه"


class Invoice(models.Model):
    date = models.DateField(verbose_name="تاریخ", db_index=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, db_index=True)
    total_amount = models.BigIntegerField(verbose_name="مبلغ کل")
    total_items = models.BigIntegerField(verbose_name="تعداد آیتم")
    total_product = models.IntegerField(null=True, blank=True, verbose_name="تعداد محصول")
    date_created = models.DateTimeField(
        null=True, default=datetime.now, verbose_name="تاریخ ساخت"
    )
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین تغییر"
    )

    class Meta:
        verbose_name = "فاکتور"
        verbose_name_plural = "فاکتور"
        indexes = [models.Index(fields=["branch", "date"])]

    def __str__(self):
        return f"{self.pk}"
    

class HolidayDate(models.Model):
    gregorian_date = models.DateField(null=True, db_index=True, verbose_name="تاریخ میلادی")
    date = models.CharField(max_length=10, verbose_name="تاریخ شمسی")

    def __str__(self):
        return self.date
    
    class Meta:
        verbose_name = "تاریخ تعطیلات"
        verbose_name_plural = "تاریخ تعطیلات"

class HolidayDescription(models.Model):
    description = models.CharField(max_length=255, verbose_name="مناسبت")
    date = models.ForeignKey(HolidayDate, on_delete=models.CASCADE, db_index=True, related_name="holidaydsc", verbose_name="تاریخ")

    def __str__(self):
        return self.description
    
    class Meta:
        verbose_name = "مناسبت تعطیلات"
        verbose_name_plural = "مناسبت تعطیلات"
        indexes = [models.Index(fields=["date"])]


class AlertCameraMalfunction(models.Model):
    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        verbose_name="مرچنت",
        db_index=True,
        blank=True,
        null=True
    )
    name = models.CharField(max_length=255, verbose_name="نام")
    mobile = models.CharField(max_length=11, verbose_name="شماره موبایل", unique=True)
    is_active = models.BooleanField(verbose_name="فعال")
    last_time_sent = models.DateTimeField(verbose_name="آخرین زمان ارسال", null=True, blank=True)
    date_created = models.DateTimeField(
        null=True, default=datetime.now, verbose_name="تاریخ ساخت"
    )
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین تغییر"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "مخاطب دریافت پیامک"
        verbose_name_plural = "مخاطب دریافت پیامک"


class AlertCameraMalfunctionMessage(models.Model):
    contact = models.ForeignKey(AlertCameraMalfunction, on_delete=models.CASCADE)
    message = models.TextField(verbose_name="متن پیام")
    date_created = models.DateTimeField(
        null=True, default=datetime.now, verbose_name="تاریخ ساخت"
    )
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین تغییر"
    )

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "پیام خطای اطلاع رسانی دوربین"
        verbose_name_plural = "پیام خطای اطلاع رسانی دوربین"


# class SendReport(models.Model):
#     merchant = models.ForeignKey(
#         Merchant,
#         on_delete=models.CASCADE,
#         verbose_name="مرچنت",
#         db_index=True,
#     )
#     name = models.CharField(max_length=255, verbose_name="نام")
#     whatsapp_mobile = models.CharField(max_length=11, verbose_name="شماره واتساپ", null=True, blank=True)
#     id_telegram = models.CharField(max_length=225, verbose_name="آی دی تلگرام", null=True, blank=True)
#     is_active = models.BooleanField(verbose_name="فعال")
#     time_sent = models.TimeField(verbose_name="زمان ارسال")
#     date_created = models.DateTimeField(
#         null=True, default=datetime.now, verbose_name="تاریخ ساخت"
#     )
#     last_modified = models.DateTimeField(
#         auto_now=True, verbose_name="تاریخ آخرین تغییر"
#     )
    