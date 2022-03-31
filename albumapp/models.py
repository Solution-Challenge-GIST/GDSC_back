import os

from django.db import models

# Create your models here.
from accountapp.models import User
from juniorapp.models import Junior
from seniorapp.models import Senior


class Album(models.Model):
    album_id = models.BigAutoField(primary_key=True)
    img = models.CharField(max_length=700)
    voice = models.CharField(max_length=700)

    emotion = models.CharField(max_length=30, null=True, blank=True, default='HAPPY')

    junior = models.ForeignKey(Junior, on_delete=models.CASCADE)
    senior = models.ForeignKey(Senior, on_delete=models.CASCADE)

    is_replied = models.BooleanField(default=False)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

def get_albumvoice_upload_path(instance, filename):
    return os.path.join(
        "albums", "voices", "%s" % filename)


class AlbumVoice(models.Model):
    albumvoice_id = models.BigAutoField(primary_key=True)
    voice = models.FileField(upload_to=get_albumvoice_upload_path)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)


def get_albumimage_upload_path(instance, filename):
    return os.path.join(
      "albums", "images", "%s" %filename)


class AlbumImage(models.Model):
    albumimage_id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to=get_albumimage_upload_path)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
