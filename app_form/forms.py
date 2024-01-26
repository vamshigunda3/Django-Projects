from dataclasses import fields
from django import forms
from .models import ImageInfo, UserInformation, CollegeInfo, EducationInfo, Vegetables


class UserInformationModelForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        form_name = "User Information"
        fields = ["name", "gender", "age", "region", "state", "coursename", "cover"]


class CollegeInfoModelForm(forms.ModelForm):
    class Meta:
        model = CollegeInfo
        form_name = "College Information"
        fields = "__all__"


class EducationInfoModelForm(forms.ModelForm):
    class Meta:
        model = EducationInfo
        form_name = "Personal Information"
        fields = [
            "group",
            "previous_college_name",
            "status",
        ]


class ImageModelForm(forms.ModelForm):
    class Meta:
        model = ImageInfo
        fields = ["photo_upload"]


class VegetableModelForm(forms.ModelForm):
    class Meta:
        model = Vegetables
        fields = "__all__"
