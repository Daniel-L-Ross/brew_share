from django.db import models
from django.contrib.auth.models import User

class Brewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50, blank=True)
    is_admin = models.BooleanField()
    profile_image = models.ImageField(
        upload_to='user_pics/%Y/%m/%d', height_field=None,
        width_field=None, max_length=None, null=True)
    current_coffee = models.CharField(max_length=50, blank=True)
    current_brew_method = models.CharField(max_length=50, blank=True)
    private = models.BooleanField()