from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class Payment(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.CharField(
        max_length=50, default=10
    )  # models.DecimalField(max_digits=10, decimal_places=2, default=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    timestamp = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(
        max_length=50, default=10
    )  # models.IntegerField(validators=[RegexValidator(r"^[0-9]*$", message="Phone number must contain only digits")],help_text="Enter your phone number",)
    date_of_birth = models.DateField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # Add any other fields relevant to your payment tracking

    def __str__(self):
        return f"{self.user.username} - {self.transaction_id}"
