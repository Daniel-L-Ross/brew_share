from django.db import models

class EntryStep(models.Model):
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE)
    step_image = models.ImageField(
        upload_to='step_pics/%Y/%m/%d', height_field=None,
        width_field=None, max_length=None, null=True, blank=True)
    descriptor = models.CharField(max_length=30)
    instruction = models.CharField(max_length=255)
    seconds = models.IntegerField()