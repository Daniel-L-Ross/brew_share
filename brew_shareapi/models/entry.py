from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Entry(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    coffee = models.ForeignKey("Coffee", on_delete=models.DO_NOTHING)
    method = models.ForeignKey("BrewMethod", on_delete=models.DO_NOTHING)
    grind_size = models.CharField(max_length=25)
    title = models.CharField(max_length=50)
    tasting_notes = models.CharField(max_length=50)
    review = models.CharField()
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],)
    setup = models.CharField()
    date = models.DateField()
    water_temp = models.IntegerField()
    water_volume = models.IntegerField()
    private = models.BooleanField()
    block = models.BooleanField()
    recipe = models.BooleanField()
    recommend = models.BooleanField()
    
    class Meta:
        verbose_name_plural = 'entries'