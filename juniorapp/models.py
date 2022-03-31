from django.db import models

# Create your models here.
from accountapp.models import User

class Junior(models.Model):
    junior_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.CharField(max_length=700, default="https://groupby-image-bucket.s3.ap-northeast-2.amazonaws.com/startup/profile/default.png")
    name = models.CharField(max_length=10, null=True)
