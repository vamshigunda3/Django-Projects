from django.urls import path
from .views import (
    form_entry_view,
    form_preview,
    handle_payment_request_view,
    payment_canceled,
    payment_completed,
)

app_name = "stripe_payment"

urlpatterns = [
    path("payment_form/", form_entry_view, name="payment_form"),
    path("form_preview/", form_preview, name="form_preview"),  # Keep this for preview
    path(
        "handle_payment/",
        handle_payment_request_view,
        name="handle_payment_request",
    ),
    path("completed/", payment_completed, name="completed"),
    path("canceled/", payment_canceled, name="canceled"),
]
