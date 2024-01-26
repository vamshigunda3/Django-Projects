# accounts/forms.py

from django import forms
from .models import UserProfile
from django.forms.widgets import SelectDateWidget


class SignupForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone_number", "date_of_birth"]
        widgets = {"date_of_birth": SelectDateWidget(years=range(1900, 2014))}
