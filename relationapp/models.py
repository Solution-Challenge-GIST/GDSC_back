from django.db import models

# Create your models here.
from juniorapp.models import Junior
from seniorapp.models import Senior


class Relation(models.Model):
    relation_id = models.BigAutoField(primary_key=True)
    junior = models.ForeignKey(Junior, on_delete=models.CASCADE)
    senior = models.ForeignKey(Senior, on_delete=models.CASCADE)
    relation = models.CharField(max_length=100)