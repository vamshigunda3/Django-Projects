from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from exam import settings
from .forms import (
    ImageModelForm,
    UserInformationModelForm,
    CollegeInfoModelForm,
    EducationInfoModelForm,
)
from django.template.loader import render_to_string
import xhtml2pdf.pisa as pisa
import io
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
import os
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def pdf_generation(form, html_url):
    capitalized_data = {
        str(key).capitalize(): str(value).capitalize()
        if isinstance(value, str)
        else value
        for key, value in form.cleaned_data.items()
    }
    print(type(capitalized_data), "Capitalised data type", capitalized_data)
    template_data = {"form_data": capitalized_data}
    print(type(template_data), "template data type", template_data)
    html = render_to_string(html_url, template_data)
    print("Printing html data", html)
    print(template_data, html)
    ## Generate pdf
    result = io.BytesIO()
    pdf = pisa.CreatePDF(html, dest=result)
    print(pdf, "trying to print pdf created through html")
    return pdf, result


from django.conf import settings


def link_callback(uri, rel):
    """Convert HTML URIs to absolute system paths, considering Django settings."""

    sUrl = settings.STATIC_URL  # "static/"
    sRoot = settings.STATICFILES_DIRS[0]  # BASE_DIR / "static"

    # Handle media files if needed (adjust MEDIA_URL and MEDIA_ROOT)
    mUrl = settings.MEDIA_URL  # Typically '/media/'
    mRoot = settings.MEDIA_ROOT  # Typically '/path/to/media/'
    print("Iam in linkcallback", sUrl)

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # Handle absolute uri (e.g., http://some.tld/foo.png)

        # Ensure the image exists
    if not os.path.isfile(path):
        raise Exception("media URI must start with %s or %s" % (sUrl, mUrl))
    print("Here is the path", path)
    return path


def pdf_generation_multi(data, html_template_path):
    """Generates a PDF from multiple data sources and a template."""

    # Combine data dictionaries for simplified template access (optional approach)
    combined_data = {**data[0], **data[1], **data[2]}

    # Render HTML template
    try:
        html = render_to_string(html_template_path, {"data": combined_data})
    except Exception as e:
        print("Error rendering HTML template:", e)
        return None, None

    # Create PDF using pisa
    result = io.BytesIO()
    try:
        pdf = pisa.CreatePDF(
            html, dest=result, encoding="utf-8", link_callback=link_callback
        )
    except Exception as e:
        print("Error generating PDF:", e)
        return None, None

    return pdf, result


# Create your views here.
def homepageview(request):
    return HttpResponse("Hello World")


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


# @login_required()
def register(request):
    print("View accessed and authenticated")
    if not request.session.get_expiry_age() > 0:
        # Redirect to logout or login page
        return redirect("home")
    if request.method == "POST":
        form = UserInformationModelForm(request.POST)

        if form.is_valid():
            # form.save()
            print("I am here")
            pdf, result = pdf_generation(form, "pdf.html")
            if not pdf.err:
                print("PDF GENERATION IN PROCESS")
                return HttpResponse(result.getvalue(), content_type="application/pdf")
            else:
                return HttpResponse("Error generating PDF".format(pdf.err))
    form = UserInformationModelForm()
    return render(request, "register.html", {"form": form})


def Image_view(request):
    if request.method == "POST":
        form = ImageModelForm(request.POST, request.FILES)
        print("checking if the form is valid")
        if form.is_valid():
            form.save()
            return redirect(
                "success-url"
            )  # Redirect to a success URL upon successful form submission
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors in the console for debugging
    else:
        form = ImageModelForm()
    return render(request, "msf_2.html", {"form": form})


from django.http import JsonResponse

from django.views.decorators.http import require_POST


# @method_decorator(login_required, name="dispatch")
class MultiStepForm(SessionWizardView):
    print("I am in the class now")
    form_list = [
        UserInformationModelForm,
        CollegeInfoModelForm,
        EducationInfoModelForm,
    ]
    template_name = "msf_1.html"
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, "covers")
    )

    # def get(self, request, *args, **kwargs):
    #     if self.request.GET.get("preview") == "true":
    #         return self.generate_preview(request)  # Handle preview request
    #     else:
    #         return super().get(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        preview_data = {}
        form_names = {
            step_name: form_class.Meta.form_name
            for step_name, form_class in self.form_list.items()
        }
        for step_name, step_form in self.form_list.items():
            cleaned_data = self.get_cleaned_data_for_step(step_name)
            form_name = form_names[step_name]  # Retrieve form name
            preview_data[form_name] = cleaned_data
            print(preview_data)
        context["preview_data"] = preview_data
        return context

    # def get_context_data(self, form, **kwargs):
    #     context = super().get_context_data(form=form, **kwargs)
    #     if self.steps.current == self.steps.last and self.request.method == "POST":
    #         preview_data = {}
    #         for step_num, form_class in enumerate(self.form_list, start=1):
    #             form_instance = self.get_cleaned_data_for_step(str(step_num))
    #             if form_instance:
    #                 form_name = (
    #                     form_class.Meta.form_name
    #                     if hasattr(form_class.Meta, "form_name")
    #                     else f"Form {step_num}"
    #                 )
    #                 preview_data[form_name] = form_instance.cleaned_data
    #         context["preview_data"] = preview_data
    #     return context
    # @require_POST
    # def generate_preview(self, request):
    #     preview_data = self.generate_preview()
    #     return JsonResponse(preview_data)

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]
        print(form_data)
        return render(self.request, "preview.html", {"preview_data": form_data})
        # Check for "submit=true" query parameter
        # if self.request.GET.get("submit") == "true":
        #     pdf, result = pdf_generation_multi(form_data, "pdf_multi.html")
        #     if not pdf.err:
        #         return HttpResponse(result.getvalue(), content_type="application/pdf")
        #     else:
        #         return HttpResponse("Error generating PDF".format(pdf.err))

        # Otherwise, proceed with normal view logic
        # return render(self.request, "msf_1.html", {"form_data": form_data})

    # def done(self, form_list, **kwargs):
    #     form_data = [form.cleaned_data for form in form_list]
    #     print(form_data, "Printing form data of multistepform")
    #     return generate_preview()
    # pdf, result = pdf_generation_multi(form_data, "pdf_multi.html")
    # if not pdf.err:
    #     print("PDF GENERATION IN PROCESS in multiform")
    #     # response = HttpResponse(pdf, content_type="application/pdf")
    #     # response['Content-Disposition'] = 'attachment; filename="generated_pdf.pdf"'
    #     return HttpResponse(result.getvalue(), content_type="application/pdf")
    # else:
    #     return HttpResponse("Error generating PDF".format(pdf.err))
    # return render(self.request, "msf_1.html", {"form_data": form_data})


def pdf_demo(html_template_path):
    x = {
        "Name": "Sdf",
        "Gender": "Female",
        "Age": 23,
        "Region": "Sdf",
        "State": "Sdf",
        "Coursename": "Sdf",
        "Cover": "present",
    }
    combined_data = [x]
    print(combined_data, "This is data from pdf_demo")
    try:
        html = render_to_string(html_template_path, {"data": combined_data})
    except Exception as e:
        print("Error rendering HTML template:", e)
        return None, None
    print(html, "This is html from pdf_demo")
    # Create PDF using pisa
    result = io.BytesIO()
    try:
        pdf = pisa.CreatePDF(
            html, dest=result, encoding="utf-8", link_callback=link_callback
        )
    except Exception as e:
        print("Error generating PDF:", e)
        return None, None

    return pdf, result


def pdf_caller(request):
    if request.method == "POST":
        pdf, result = pdf_demo("pdf_demo.html")
        if not pdf.err:
            print("PDF GENERATION IN PROCESS in multiform")
            return HttpResponse(result.getvalue(), content_type="application/pdf")
        else:
            return HttpResponse("Error generating PDF".format(pdf.err))
    return render(request, "pdf_caller.html")
