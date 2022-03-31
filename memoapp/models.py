from django.db import models

# Create your models here.
from albumapp.models import Album
from juniorapp.models import Junior


class Memo(models.Model):
    memo_id = models.BigAutoField(primary_key=True)

    emotion = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField(default='', null=True, blank=True)

    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True)
    junior = models.ForeignKey(Junior, on_delete=models.SET_NULL, null=True)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)