# Generated by Django 4.2.8 on 2024-01-19 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="amount",
            field=models.CharField(default=10, max_length=50),
        ),
        migrations.AlterField(
            model_name="payment",
            name="phone_number",
            field=models.CharField(default=10, max_length=50),
        ),
    ]
