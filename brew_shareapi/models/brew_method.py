from django.db import models

class BrewMethod(models.Model):
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    method_image = models.ImageField(
        upload_to='coffee_pics/%Y/%m/%d', height_field=None,
        width_field=None, max_length=None, null=True)
    website = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("brewmethod")
        verbose_name_plural = ("brewmethods")