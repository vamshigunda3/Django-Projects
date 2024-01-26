from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class payments(models.Model):
    amount = models.CharField(max_length=50, default=10)
    phone_number = models.CharField(max_length=50, default=10)
    date_of_birth = models.DateField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # Add any other fields relevant to your payment tracking

    # def __str__(self):
    #     return f"{self.user.username} - {self.transaction_id}"
