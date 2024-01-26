from django.contrib import admin

# Register your models here.
from .models import UserInformation, CollegeInfo, EducationInfo, ImageInfo, Vegetables

# from .forms import UserInformationModelForm

admin.site.register(UserInformation)
admin.site.register(CollegeInfo)
admin.site.register(EducationInfo)
admin.site.register(ImageInfo)
admin.site.register(Vegetables)
# admin.site.register(UserInformationModelForm)
