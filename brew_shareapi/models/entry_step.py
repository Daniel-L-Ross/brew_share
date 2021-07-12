from django.db import models
import cloudinary
import environ
env = environ.Env()
environ.Env.read_env()

cloudinary.config(cloud_name = 'brewshare',
                        api_key = env("CLOUDINARY_API_KEY"),
                        api_secret = env("CLOUDINARY_SECRET_KEY"))


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
            cloudinary.uploader.destroy(self.cloudinary_image_id)
        super(EntryStep, self).delete()