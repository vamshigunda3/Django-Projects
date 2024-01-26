from django.db import models
import uuid

# Create your models here.


class CollegeInfo(models.Model):
    college_name = models.CharField(max_length=255)
    course_offered = models.CharField(max_length=255)
    city = models.CharField(max_length=15)
    district = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.college_name} - {self.course_offered} - {self.city} - {self.district}"


class UserInformation(models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=50,
        choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
    )
    age = models.PositiveIntegerField()
    region = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    coursename = models.CharField(max_length=255)
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, blank=True
    )
    cover = models.ImageField(upload_to="covers/")

    # tried this feature
    college = models.ForeignKey(CollegeInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.coursename}"

    # Add additional models if needed...


class EducationInfo(models.Model):
    group = models.CharField(max_length=15)
    previous_college_name = models.CharField(max_length=15)
    status = models.CharField(
        max_length=50,
        choices=(("Pass", "Pass"), ("Fail", "Fail"), ("Other", "Other")),
    )
    user = models.ForeignKey(UserInformation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.group} - {self.previous_college_name} - {self.status}"


class ImageInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo_upload = models.ImageField(upload_to="covers/")


class Vegetables(models.Model):
    name = models.CharField(max_length=15)
