from django.db import models

# Create your models here.
from accountapp.models import User
from juniorapp.models import Junior


class Senior(models.Model):
    senior_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.CharField(max_length=700, default="https://groupby-image-bucket.s3.ap-northeast-2.amazonaws.com/startup/profile/default.png", blank=True, null=True)
    name = models.CharField(max_length=10, null=True)
    age = models.IntegerField()
    address = models.CharField(max_length=500, null=True, blank=True)
    illness = models.CharField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    remarks = models.CharField(max_length=3000, null=True, blank=True)





