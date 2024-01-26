from decimal import Decimal
import json
import uuid
from django.shortcuts import get_object_or_404, render

# Create your views here.

from ast import Break
from typing import final
from django.shortcuts import render, redirect, reverse

from exam import settings
from .forms import PaymentRegistrationForm
from .models import payments
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
import logging
from django.contrib import messages
from urllib.parse import urlencode
import stripe  # Import the Stripe library
from django.db import models

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def form_entry_view(request):
    if request.method == "POST":
        form = PaymentRegistrationForm(request.POST)
        if form.is_valid():
            payment_data = form.save()
            payment_data_id = payment_data.phone_number
            print(payment_data, ": Payment_data")
            request.session["payment_data_id"] = payment_data_id
            return redirect("stripe_payment:form_preview")
    else:
        form = PaymentRegistrationForm()
    return render(request, "stripe_payment/payment_form.html", {"form": form})


def form_preview(request):
    print("I am in form_preview")
    payment_data = request.session.get("payment_data_id")
    form_data_objects = payments.objects.filter(phone_number=payment_data)
    if form_data_objects:
        # Sort by timestamp and select the most recent:
        form_data = form_data_objects.last()
        print(form_data)
    print(payment_data)
    return render(
        request, "stripe_payment/form_preview.html", {"payment_data": form_data}
    )


def handle_payment_request_view(request):
    """
    Handles the payment request initiated from the preview page.
    Args:
        request (HttpRequest): The incoming HTTP request.
        payment_id (int): The ID of the payment to be processed.
    Returns:
        HttpResponse: Redirects to Stripe's payment page or renders an error page.
    """
    # Retrieve payment data from the database
    payment_id = request.POST.get("payment_id")
    form_data_objects = payments.objects.filter(phone_number=payment_id)
    if form_data_objects:
        # Sort by timestamp and select the most recent:
        form_data = form_data_objects.last()
        print(form_data, "This is form data in hprv")
    if request.method == "POST":
        success_url = request.build_absolute_uri(reverse("stripe_payment:completed"))
        cancel_url = request.build_absolute_uri(reverse("stripe_payment:canceled"))
        customer = stripe.Customer.create(
            name="Jenny Rosen",
            address={
                "line1": "510 Townsend St",
                "postal_code": "98140",
                "city": "San Francisco",
                "state": "CA",
                "country": "US",
            },
        )
        # Stripe checkout session data
        session_data = {
            "mode": "payment",
            "customer": customer,
            "client_reference_id": form_data.phone_number,
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [],
        }

        session_data["line_items"].append(
            {
                "price_data": {
                    "unit_amount": int(int(form_data.amount) * Decimal("100")),
                    "currency": "inr",
                    "product_data": {
                        "name": "entry",
                    },
                },
                "quantity": 1,
            }
        )

        #  "name": "vamshi",
        #         "address": {
        #             "line1": "Greater Kailash",  # Replace with the appropriate field names
        #             "city": "Delhi",
        #             "state": "Delhi",
        #             "postal_code": "00000",
        #             "country": "GA",
        #         },
        print("Session_data", session_data)

        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # redirect to Stripe payment form
        return redirect(session.url, code=303)
    else:
        return render(
            request,
            "payment/process.html",
        )


def payment_completed(request):
    data = request.session
    print(data)
    return render(request, "stripe_payment/completed.html")


def payment_canceled(request):
    return render(request, "stripe_payment/canceled.html")
