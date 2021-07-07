from django.db import models

class EntryStep(models.Model):
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE)
    step_image = models.URLField(blank=True)
    cloudinary_image_id = models.CharField(max_length=255, blank=True)
    descriptor = models.CharField(max_length=30)
    instruction = models.CharField(max_length=255)
    seconds = models.IntegerField()

    # TODO: add logic to delete entry step photo when the corresponding entry is deleted.
    # def delete(self):
    #     if self.step_image:
    #         pass
    #     super(EntryStep, self).delete()