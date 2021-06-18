from django.db import models

class BrewMethod(models.Model):
    brewer = models.ForeignKey('Brewer', on_delete=models.DO_NOTHING)
    method_image = models.ImageField(
        upload_to='method_pics/%Y/%m/%d', height_field=None,
        width_field=None, max_length=None, null=True, blank=True)
    website = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=50)