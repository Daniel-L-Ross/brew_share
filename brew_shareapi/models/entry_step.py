from django.db import models
from brew_shareapi.image_handler import cloudinary_delete

class EntryStep(models.Model):
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE)
    step_image = models.URLField(blank=True)
    cloudinary_image_id = models.CharField(max_length=255, blank=True)
    descriptor = models.CharField(max_length=30)
    instruction = models.CharField(max_length=255)
    seconds = models.IntegerField()

# override the default delete to handle deletion of photos stored on cloudinary
    def delete(self):
        if self.step_image:
            cloudinary_delete(self.cloudinary_image_id)
        super(EntryStep, self).delete()