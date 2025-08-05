from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
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
        return f"{self.merchant.name} | {self.name}"

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

    def __str__(self):
        return f"{self.cam_name} {self.ip}"

    class Meta:
        verbose_name = "دوربین"
        verbose_name_plural = "دوربین"


class PeopleCounting(models.Model):  # former name: Stats
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


class Campaign(models.Model):
    campaign_types = [("ویترین", "ویترین"), ("فروش", "فروش")]
    name = models.CharField(max_length=255, verbose_name="نام کمپین")
    start_date = models.DateField(verbose_name="تاریخ")
    end_date = models.DateField(verbose_name="تاریخ پایان", null=True, blank=True)
    campaign_type = models.CharField(
        choices=campaign_types,
        null=True,
        blank=True,
        max_length=10,
        verbose_name="نوع کمپین",
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="شعبه")
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
    date = models.DateField(verbose_name="تاریخ")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    total_amount = models.CharField(max_length=255, verbose_name="مبلغ کل")
    total_items = models.CharField(max_length=255, verbose_name="تعداد آیتم")
    date_created = models.DateTimeField(
        null=True, default=datetime.now, verbose_name="تاریخ ساخت"
    )
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین تغییر"
    )

    class Meta:
        verbose_name = "فاکتور"
        verbose_name_plural = "فاکتور"

    def __str__(self):
        return f"{self.pk}"
