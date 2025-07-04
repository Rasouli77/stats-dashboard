# Generated by Django 5.0 on 2025-05-28 17:10

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0008_remove_peoplecounting_vendor_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="defaultdate",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="branch",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(2025, 5, 28, 20, 40, 48, 866855), null=True
            ),
        ),
        migrations.AlterField(
            model_name="cam",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(2025, 5, 28, 20, 40, 48, 867325), null=True
            ),
        ),
        migrations.AlterField(
            model_name="campaigncalendar",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(2025, 5, 28, 20, 40, 48, 868382), null=True
            ),
        ),
        migrations.AlterField(
            model_name="city",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(2025, 5, 28, 20, 40, 48, 866124), null=True
            ),
        ),
        migrations.AlterField(
            model_name="country",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(2025, 5, 28, 20, 40, 48, 865470), null=True
            ),
        ),
        migrations.AlterField(
            model_name="defaultdate",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(2025, 5, 28, 20, 40, 48, 868765), null=True
            ),
        ),
        migrations.AlterField(
            model_name="district",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(2025, 5, 28, 20, 40, 48, 866471), null=True
            ),
        ),
        migrations.AlterField(
            model_name="merchant",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(2025, 5, 28, 20, 40, 48, 864999), null=True
            ),
        ),
        migrations.AlterField(
            model_name="peoplecounting",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(2025, 5, 28, 20, 40, 48, 867865), null=True
            ),
        ),
        migrations.AlterField(
            model_name="province",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(2025, 5, 28, 20, 40, 48, 865772), null=True
            ),
        ),
    ]
