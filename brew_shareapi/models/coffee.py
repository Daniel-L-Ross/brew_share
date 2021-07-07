from django.db import models

class Coffee(models.Model):
    brewer = models.ForeignKey('Brewer', on_delete=models.DO_NOTHING)
    coffee_image = models.URLField(blank=True)
    cloudinary_image_id = models.CharField(max_length=255, blank=True)
    roaster = models.CharField(max_length=50)
    website = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    process = models.CharField(max_length=50)
    recommended_method = models.CharField(max_length=50)
    tasting_notes = models.CharField(max_length=50)