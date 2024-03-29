# Generated by Django 4.2.8 on 2023-12-24 17:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="phone_number",
            field=models.IntegerField(
                help_text="Enter your phone number",
                validators=[
                    django.core.validators.RegexValidator(
                        "^[0-9]*$", message="Phone number must contain only digits"
                    )
                ],
            ),
        ),
    ]
