from ast import Break
from typing import final
from django.shortcuts import render, redirect

from exam import settings
from .forms import PaymentRegistrationForm
from .models import Payment
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
import paytm
import logging
from django.contrib import messages
from urllib.parse import urlencode

import uuid  # Import the UUID library
from app_form.views import pdf_generation

from .Checksum import generate_checksum, verify_checksum, __id_generator__
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import paytmchecksum
import urllib.parse


def generate_transaction_id():
    """Generates a unique transaction ID."""
    return str(uuid.uuid4())  # Generate a random UUID and convert to string


@csrf_exempt
def handle_paytm_response(request):
    print("I am in handle request")
    try:  # Retrieve Paytm response data
        paytm_response = request.POST
        print(paytm_response, "Paytm response")
        response_dict = {}
        if request.method == "POST":
            data_dict = {}
            for key in request.POST:
                data_dict[key] = request.POST[key]
            MID = data_dict["MID"]
            ORDERID = data_dict["ORDERID"]
            # Assuming Paytm sends data via POST
            print(paytm_response, "Paytm response")
            # Verify signature using Paytm SDK
            is_valid_response = verify_checksum(
                data_dict, settings.PAYTM_MERCHANT_KEY, data_dict["CHECKSUMHASH"]
            )
            print(is_valid_response)  # Your Paytm merchant key
            # response_data=paytm_response,
            # checksum=paytm_response.get(
            #     "CHECKSUMHASH"
            # ),  # Assuming checksum is in this field
            if is_valid_response:
                # Extract payment status and transaction ID
                payment_status = paytm_response.get(
                    "STATUS"
                )  # Replace with Paytm's status field
                transaction_id = paytm_response.get(
                    "TXNID"
                )  # Replace with Paytm's transaction ID field

                if (
                    payment_status == "TXN_SUCCESS"
                ):  # Replace with Paytm's success indicator
                    # Retrieve form data from session
                    form_data = request.session.pop("payment_form_data", {})

                    # Create payment object
                    payment = Payment.objects.create(
                        transaction_id=transaction_id,
                        status="SUCCESS",
                        user=form_data["user"],
                        amount=form_data["amount"],
                        phone_number=form_data["phone_number"],
                        date_of_birth=form_data["date_of_birth"],
                        first_name=form_data["first_name"],
                        last_name=form_data["last_name"],
                    )

                    # Create user object (using only relevant fields from form data)
                    user = User.objects.create_user(
                        username=form_data["phone_number"],
                        password=str(form_data["date_of_birth"]),
                        first_name=form_data["first_name"],
                        last_name=form_data["last_name"],
                    )

                    ### Pdf generation needs to happen here!!!!!!!!!!
                    # !!!!!!!!!!!!!!!!!!!!!
                    return render(
                        request, "payment_details.html", {"payment": payment}
                    )  # Redirect to confirmation page
                else:
                    # Handle invalid Paytm response
                    logging.error("Invalid Paytm response received: %s", paytm_response)
                    messages.error(
                        request,
                        "Invalid payment response received. Please contact support.",
                    )

                    # Handle payment failure (e.g., log error, display message)
                    # ...
            else:
                logging.error("Invalid Paytm response received: %s", paytm_response)
                messages.error(
                    request,
                    "Invalid payment response received. Please contact support.",
                )

                # Ha# Handle invalid response (e.g., log error, display message)
                # ...

    except Exception as e:
        logging.exception("An error occurred during payment processing: %s", e)
        messages.error(
            request,
            "An error occurred during payment processing. Please try again later.",
        )

    # Redirect to error page or back to payment form, depending on your preference
    return redirect("payment_error")  # Example redirection to an error page

    # def payment_registration(request):
    if request.method == "POST":
        form = PaymentRegistrationForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            amount = form.cleaned_data["amount"]  # Retrieve payment amount
            print("I have got the data")
            user_profile_exists = Payment.objects.filter(
                phone_number=phone_number, date_of_birth=date_of_birth
            ).exists()
            print("User_profile status exisiting or not", user_profile_exists)
            print(form.cleaned_data)
        try:
            if user_profile_exists:
                messages.error(
                    request,
                    "This user is already registered. Please change phone number or date of birth to continue.",
                )
                return render(request, "accounts/signup.html", {"form": form})

            paytmParams = dict()
            paytmParams["body"] = {
                "requestType": "Payment",
                "mid": settings.PAYTM_MERCHANT_ID,
                "websiteName": settings.PAYTM_WEBSITE,
                "orderId": __id_generator__(),
                "callbackUrl": settings.PAYTM_CALLBACK_URL,
                "txnAmount": {"value": "1.00", "currency": "INR"},
                "userInfo": {"custId": "CUST_001"},
            }
            print(paytmParams)
            checksum = paytmchecksum.generateSignature(
                json.dumps(paytmParams["body"]), settings.PAYTM_MERCHANT_KEY
            )
            if not paytmchecksum.validateSignature(
                json.dumps(paytmParams["body"]), settings.PAYTM_MERCHANT_KEY, checksum
            ):
                raise ValueError("Generated checksum is invalid")

            print(checksum)
            paytmParams["head"] = {"signature": checksum}

            post_data = json.dumps(paytmParams)

            # for Staging
            mid = paytmParams["body"]["mid"]
            orderId = paytmParams["body"]["orderId"]

            base_url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction"
            query_params = urllib.parse.urlencode({"mid": mid, "orderId": orderId})

            final_url = f"{base_url}?{query_params}"
            print(final_url, "final url")
            print(paytmParams, ":: All parameters")
            response = requests.post(
                final_url, data=post_data, headers={"Content-type": "application/json"}
            ).json()
            print(response)
            txnToken = response["body"]["txnToken"]  # Extract txnToken
            redirect_url = f"{final_url}&txnToken={txnToken}"
            # redirect_url = f"{url}&txnToken={txnToken}"
            print(redirect_url)
            return redirect(redirect_url)
            # redirect(
            #     request, "payments/payment_details.html", {"param_dict": paytmParams}
            # )
        #         # return redirect(request,'payments/payment_details.html', payment_url)
        # # payment_url = f"{settings.PAYTM_PAYMENT_GATEWAY_URL}{data_dict}"
        except Exception as e:
            # #     # Handle any errors during payment initiation
            print("Error during payment initiation:", e)
            messages.error(
                request,
                "An error occurred while initiating payment. Please try again.",
            )
            return render(request, "payments/payment_registration.html", {"form": form})
    else:
        form = PaymentRegistrationForm()

    return render(request, "payments/payment_registration.html", {"form": form})


def payment_registration(request):
    if request.method == "POST":
        form = PaymentRegistrationForm(request.POST)
        if form.is_valid():
            paytmParams = dict()
            paytmParams["body"] = {
                "requestType": "Payment",
                "mid": settings.PAYTM_MERCHANT_ID,
                "websiteName": settings.PAYTM_WEBSITE,
                "orderId": __id_generator__(),
                "callbackUrl": settings.PAYTM_CALLBACK_URL,
                "txnAmount": {"value": "1.00", "currency": "INR"},
                "userInfo": {
                    "custId": "CUST_789",
                },
            }
            print(paytmParams)
            checksum = paytmchecksum.generateSignature(
                json.dumps(paytmParams["body"]), settings.PAYTM_MERCHANT_KEY
            )
            print(checksum)
            if not paytmchecksum.verifySignature(
                json.dumps(paytmParams["body"]), settings.PAYTM_MERCHANT_KEY, checksum
            ):
                raise ValueError("Generated checksum is invalid")
            paytmParams["head"] = {"signature": checksum}
            post_data = json.dumps(paytmParams)

            mid = paytmParams["body"]["mid"]
            orderId = paytmParams["body"]["orderId"]
            base_url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction"
            query_params = urllib.parse.urlencode({"mid": mid, "orderId": orderId})
            final_url = f"{base_url}?{query_params}"
            # url = {"url": final_url}
            # paytmParams["url"] = final_url
            print(paytmParams, ":: All parameters")
            print(final_url)
            response = requests.post(
                final_url, data=post_data, headers={"Content-type": "application/json"}
            ).json()
            print("This is the response from Paytm:", response)
            paytmParams["body"] = {
                "mid": mid,
                "orderId": orderId,
                "returnToken": "true",
            }
            paytmParams["head"] = {
                "tokenType": "TXN_TOKEN",
                "token": response["body"]["txnToken"],
            }
            post_data = json.dumps(paytmParams)
            print("Post paytm response params", paytmParams)
            # for Staging

            url = "https://securegw-stage.paytm.in/theia/api/v2/fetchPaymentOptions"
            final_url = f"{url}?{query_params}"

            response = requests.post(
                final_url, data=post_data, headers={"Content-type": "application/json"}
            ).json()
            print(response)
            # payment_page = {
            #     "mid": mid,
            #     "txnToken": response["body"]["txnToken"],
            #     "orderId": orderId,
            # }
            # print(payment_page)
            return render(request, "payments/paytm.html", {"param_dict": paytmParams})
    else:
        print("Form is not valid")
        form = PaymentRegistrationForm()
        context = {"form": form, "amount": "10"}
    return render(request, "payments/payment_registration.html", {"form": form})

    #  paytmParams["head"] = {"signature": checksum}
    #         print(paytmParams, ":: All parameters")
    #         post_data = json.dumps(paytmParams)

    #         # for Staging
    #         mid = paytmParams["body"]["mid"]
    #         orderId = paytmParams["body"]["orderId"]
    #         base_url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction"
    #         # base_url = "https://securegw-stage.paytm.in/link/create"
    #         query_params = urllib.parse.urlencode({"mid": mid, "orderId": orderId})
    #         final_url = f"{base_url}?{query_params}"
    #         # https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={mid}&orderId={orderId}
    #         # print(final_url, "final url")

    #         response = requests.post(
    #             final_url, data=post_data, headers={"Content-type": "application/json"}
    #         ).json()

    #         print(response)
    #         txnToken = response["body"]["txnToken"]  # Extract txnToken
    #         redirect_url = f"{final_url}&txnToken={txnToken}"
    #         paytmParams["response"] = response

    #         print(redirect_url)
    #         # respone = {'head': {'responseTimestamp': '1703695475398', 'version': 'v1',
    #         #           'signature': 'oUm/QMZG8e/IgQ8woAsX9CMuzni7wnC/lyxNDGVsFD2AeMcjic5XglcBIHCdlE5+PMoIV+zKaEo+c2ELIsFBh5l+ymhjAOQGgqISzVjU770='},
    #         #           'body': {'resultInfo': {'resultStatus': 'S', 'resultCode': '0000', 'resultMsg': 'Success'},
    #         #                    'txnToken': '3a7eda4a775244af86b8009192bf150a1703695475288', 'isPromoCodeValid': False, 'authenticated': False}}
    #         postpaytmParams = dict()

    #         postpaytmParams["body"] = {
    #             "mid": mid,
    #             "orderId": orderId,
    #             "returnToken": "true",
    #         }
    #         postpaytmParams["head"] = {
    #             "tokenType": "TXN_TOKEN",
    #             "token": response["body"]["txnToken"],
    #         }
    #         print(postpaytmParams)
    #         post_response_data = json.dumps(postpaytmParams)


# https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid={{urllib.parse.quote_plus(param_dict.body.mid)}}&orderId={{urllib.parse.quote_plus(param_dict.body.orderId)}}
##url creation
# paytmParams["encoded_mid"]: {
#     urllib.parse.quote_plus(paytmParams["body"]["mid"]),
# }
# paytmParams["encoded_orderId"]: {
#     urllib.parse.quote_plus(paytmParams["body"]["orderId"]),
# }
#         # for Staging
#         payment_url = (
#             "https://securegw-stage.paytm.in/theia/api/v2/fetchPaymentOptions"
#         )
#         finalpl = f"{payment_url}?{query_params}"
#         print("I am at final pl")
#         # for Production
#         # url = "https://securegw.paytm.in/theia/api/v2/fetchPaymentOptions?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
#         payment_response = requests.post(
#             finalpl,
#             data=post_response_data,
#             headers={"Content-type": "application/json"},
#         ).json()
#         print("Payment_response:", payment_response)
#         # return redirect(finalpl)
#         # return redirect(request, "payments/paytm.html", {"param_dict": paytmParams})
