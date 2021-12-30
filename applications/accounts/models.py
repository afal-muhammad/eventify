from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class User(AbstractUser, TimeStampModel):
    image = models.ImageField(upload_to='profile', null=True, blank=True)

    def __str__(self):
        return self.first_name