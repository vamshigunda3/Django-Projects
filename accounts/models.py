from django.db import models

# Create your models here.
# Inside models.py in the 'accounts' app

from django.db import models
from django.core.validators import RegexValidator
from django.forms.widgets import SelectDateWidget


class UserProfile(models.Model):
    # Add additional fields as needed
    phone_number = models.IntegerField(
        validators=[
            RegexValidator(r"^[0-9]*$", message="Phone number must contain only digits")
        ],
        help_text="Enter your phone number",
    )
    date_of_birth = models.DateField()

    # Add any other fields relevant to the user profile

    def __str__(self):
        return self.phone_number + "'s Profile"
