from django import forms
from .models import payments
from django.forms.widgets import SelectDateWidget


class PaymentRegistrationForm(forms.ModelForm):
    class Meta:
        model = payments
        fields = ["first_name", "last_name", "phone_number", "date_of_birth", "amount"]
        widgets = {"date_of_birth": SelectDateWidget(years=range(1900, 2014))}

    def __init__(self, *args, **kwargs):
        super(PaymentRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["amount"].widget.attrs["readonly"] = True
