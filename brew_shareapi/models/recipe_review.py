from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class RecipeReview(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE)
    review = models.CharField()
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],)

    class Meta:
        verbose_name = ("recipereview")
        verbose_name_plural = ("recipereviews")

