# Generated by Django 5.0 on 2025-05-13 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stats',
            name='entry',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='stats',
            name='invoice_count',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='stats',
            name='invoice_item',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='stats',
            name='date',
            field=models.DateField(),
        ),
    ]
