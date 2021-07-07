from django.db import models
from django.contrib.auth.models import User

class Brewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50, blank=True)
    is_admin = models.BooleanField()
    profile_image = models.URLField(blank=True)
    cloudinary_image_id = models.CharField(max_length=255, blank=True)
    current_coffee = models.CharField(max_length=50, blank=True)
    current_brew_method = models.CharField(max_length=50, blank=True)
    private = models.BooleanField(null=True)
    favorites = models.ManyToManyField('Entry', through='FavoriteEntry', related_name='liked')

    # TODO: add properties to get firstname lastname username