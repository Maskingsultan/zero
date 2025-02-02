import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Customer(models.Model):
    email = models.EmailField()
    password = models.TextField()

    def __str__(self):
        return self.email


class Extended(models.Model):
    id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    img = models.ImageField()

    def __str__(self):
        return str(self.id)


@receiver(pre_delete, sender=User)
def remove_picture(sender, instance, **kwargs):
    try:
        os.remove(instance.extended.img.path)
    except:
        pass