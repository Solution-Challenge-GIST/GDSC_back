import os

from django.db import models

# Create your models here.
from accountapp.models import User
from albumapp.models import Album
from seniorapp.models import Senior


class Reply(models.Model):
    reply_id = models.BigAutoField(primary_key=True)
    voice = models.CharField(max_length=700)

    emotion = models.CharField(max_length=30, null=True, blank=True, default='SOSO')

    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)


def get_replyvoice_upload_path(instance, filename):
    return os.path.join(
        "albums", "%s" % instance.album_id, "replies", "%s" % filename)


class ReplyVoice(models.Model):
    replyvoice_id = models.BigAutoField(primary_key=True)
    voice = models.FileField(upload_to=get_replyvoice_upload_path)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

