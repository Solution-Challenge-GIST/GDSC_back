import os

from django.db import models

# Create your models here.
from accountapp.models import User
from albumapp.models import Album
from juniorapp.models import Junior
from seniorapp.models import Senior


class SimpleVoice(models.Model):
    simplevoice_id = models.BigAutoField(primary_key=True)
    voice = models.CharField(max_length=700)

    emotion = models.CharField(max_length=30, null=True, blank=True, default='SAD')

    junior = models.ForeignKey(Junior, on_delete=models.SET_NULL, null=True)
    senior = models.ForeignKey(Senior, on_delete=models.SET_NULL, null=True)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)


def get_simplevoice_upload_path(instance, filename):
    return os.path.join(
        "seniors", "%s" % instance.senior_id, "simplevoices", "%s" % filename)


class SimpleVoiceFile(models.Model):
    simplevoicefile_id = models.BigAutoField(primary_key=True)
    voice = models.FileField(upload_to=get_simplevoice_upload_path)

    senior = models.ForeignKey(Senior, on_delete=models.SET_NULL, null=True)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
