from django.db import models

class BrewMethod(models.Model):
    brewer = models.ForeignKey('Brewer', on_delete=models.DO_NOTHING)
    method_image = models.URLField(blank=True)
    website = models.URLField(blank=True)
    name = models.CharField(max_length=50)