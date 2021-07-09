from django.db import models
import cloudinary
import environ
env = environ.Env()
environ.Env.read_env()

cloudinary.config(cloud_name = 'brewshare',
                        api_key = env("CLOUDINARY_API_KEY"),
                        api_secret = env("CLOUDINARY_SECRET_KEY"))


# override the default delete on a queryset to handle cascade deletion of photos stored on cloudinary
class EntryStepQuerySet(models.QuerySet):
    def delete(self):
        for obj in self:
            if obj.step_image:
                test_variable = cloudinary.uploader.destroy(self.cloudinary_image_id)
                print(test_variable)
        super(EntryStepQuerySet, self).delete()

class EntryStep(models.Model):
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE)
    step_image = models.URLField(blank=True)
    cloudinary_image_id = models.CharField(max_length=255, blank=True)
    descriptor = models.CharField(max_length=30)
    instruction = models.CharField(max_length=255)
    seconds = models.IntegerField()

    def delete(self):
        if self.step_image:
            test_variable = cloudinary.uploader.destroy(self.cloudinary_image_id)
            print(test_variable)
        super(EntryStep, self).delete()