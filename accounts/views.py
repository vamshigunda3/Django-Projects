# Create your views here.
# accounts/views.py
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import UserProfile
from datetime import datetime

# Inside your view function
# Convert date_of_birth to a string before storing it in the session


from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login


def payment_confirmation(request):
    # Retrieve stored data from the session
    print("I am in payment confirmation")
    phone_number = request.session.get("phone_number")
    # Inside your payment_confirmation view function
    # Retrieve stored data from the session and convert date_of_birth back to a date object
    date_of_birth = datetime.strptime(
        request.session.get("date_of_birth"), "%Y-%m-%d"
    ).date()

    payment_is_successful = True
    # Check if payment is successful (hypothetical check)
    if (
        payment_is_successful
    ):  # Replace 'payment_is_successful' with your logic to check payment success
        # Create a user with phone number as the username and date of birth as the password
        user = User.objects.create_user(
            username=phone_number, password=str(date_of_birth)
        )
        form_data = {"phone_number": phone_number, "date_of_birth": date_of_birth}
        form = SignupForm(form_data)
        print("Data is saved!!!")
        if form.is_valid():
            # Save the form data to create a user
            form.save()

        # Additional processing or saving related data to UserProfile or other models

        return HttpResponse(
            "signup_success"
        )  # Redirect to success page after successful signup
    else:
        # Handle payment failure scenario
        # Redirect or render an appropriate page indicating payment failure
        messages.error(
            request,
            "This user is already registered. Please change phone number or date of birth to continue.",
        )
        return HttpResponse("Sign is Unsuccessful :( Please Try again")


# def payment_status(request):
#     if payment_is_successful:
#         request.session["payment_successful"] = True
#         # Other actions after successful payment

#     return redirect('signup')


# def signup(request):
#     if request.method == "POST":
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             phone_number = form.cleaned_data["phone_number"]
#             date_of_birth = form.cleaned_data["date_of_birth"]
#             print("I have got the data")
#             # Check if a user with the given phone number (username) and password exists
#             user_exists = User.objects.filter(username=phone_number).exists()
#             print(user_exists, ":This is user_exists")
#             print("this is date of birth as entered", date_of_birth)
#             if user_exists:
#                 user = User.objects.get(username=phone_number)
#                 print("I am in userexists")
#                 if check_password(str(date_of_birth), user.password):
#                     print(
#                         "The pass word is",
#                         check_password(str(date_of_birth), user.password),
#                         user.password,
#                         date_of_birth.isoformat(),
#                         date_of_birth,
#                     )
#                     messages.error(
#                         request,
#                         "This user is already registered. Please change phone number or date of birth to continue.",
#                     )
#                     # return HttpResponse("User exists")
#                     return render(
#                         request, "accounts/signup.html", {"form": form}
#                     )  # Render signup page with error message
#             user = User.objects.create_user(
#                 username=phone_number, password=str(date_of_birth)
#             )
#             print(user.objects.all())
#             form.save()
#             print(
#                 "User check finished!!!!"
#             )  # If no matching user found, redirect to the payment confirmation page
#             # request.session["phone_number"] = phone_number  # Store data in session for payment verification
#             # request.session["date_of_birth"] = date_of_birth.isoformat()
#             # print("I finished request session")
#             return redirect(
#                 "payment_confirmation"
#             )  # Redirect to payment confirmation page
#     else:
#         form = SignupForm()

#     return render(request, "accounts/signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        print(form)
        print("Is the form valid?", form.is_valid())
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            # Authenticate user based on entered phone number and date of birth
            user = User.objects.filter(username=phone_number).first()
            if user and user.check_password(str(date_of_birth)):
                login(request, user)
                print("All good with the log in page")
                return redirect("app_form:msf_1")
            if user:
                messages.error(
                    request,
                    "Please check the password",
                )  # Invalid credentials # Redirect to success page or dashboard success page or a dashboard
                return render(
                    request,
                    "accounts/login.html",
                    {"form": form, "error": "Invalid credentials"},
                )
        messages.error(
            request,
            "Something is wrong",
        )  # Invalid credentials
        return render(
            request,
            "accounts/login.html",
            {"form": form, "error": "Invalid credentials"},
        )
    else:
        form = SignupForm()
    return render(request, "accounts/login.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            print("I have got the data")

            # Check if a user profile with the given phone number and date of birth exists
            user_profile_exists = UserProfile.objects.filter(
                phone_number=phone_number, date_of_birth=date_of_birth
            ).exists()
            print("User_profile status exisiting or not", user_profile_exists)
            if user_profile_exists:
                messages.error(
                    request,
                    "This user is already registered. Please change phone number or date of birth to continue.",
                )
                return render(
                    request, "accounts/signup.html", {"form": form}
                )  # Render signup page with error message

            # Create a user profile
            user = User.objects.create_user(
                username=phone_number, password=str(date_of_birth)
            )
            print("user is created username and password is registered")
            form.save()

            # Additional processing or saving related data to UserProfile or other models
            print("User profile created!")

            # Redirect to the payment confirmation page
            return HttpResponse("User is Created")  # redirect("payment_confirmation")

    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})
