from django.db import models
from django.conf import settings
import os

# Create your models here.
class Image(models.Model):
    img = models.ImageField(upload_to='images/')