# accounts/urls.py

from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path(
        "payment-confirmation/", views.payment_confirmation, name="payment_confirmation"
    ),
    path("login/", views.user_login, name="login")
    # Add other URLs related to accounts here if needed
]
