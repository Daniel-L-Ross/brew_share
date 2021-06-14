from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class RecipeReview(models.Model):
    brewer = models.ForeignKey('Brewer', on_delete=models.CASCADE)
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE)
    review = models.CharField(max_length=255)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],)