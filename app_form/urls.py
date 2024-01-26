from django.urls import path
from .views import (
    homepageview,
    HomePageView,
    AboutPageView,
    register,
    MultiStepForm,
    Image_view,
    pdf_caller,
)

app_name = "app_form"

urlpatterns = [
    path("initial/", homepageview, name="initial"),
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("register/", register, name="register"),
    path("msf_2/", Image_view, name="msf_2"),
    path("msf_1/", MultiStepForm.as_view(), name="msf_1"),
    path("pdf_caller/", pdf_caller, name="pdf_caller"),
    path("generate_preview/", MultiStepForm.as_view(), name="generate_preview"),
]
