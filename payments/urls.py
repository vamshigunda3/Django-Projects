from django.urls import path
from .views import payment_registration, handle_paytm_response

app_name = "payments"

urlpatterns = [
    path("payment_registration/", payment_registration, name="payment_registration"),
    path("response/", handle_paytm_response, name="handle_paytm_response"),
]
