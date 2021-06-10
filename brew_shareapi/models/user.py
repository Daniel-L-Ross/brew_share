from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=250)
    is_admin = models.BooleanField()
    profile_image = models.ImageField()