from django.db import models

class RecommendRecipe(models.Model):
    recommender = models.ForeignKey('Brewer', related_name='recommender', on_delete=models.DO_NOTHING)
    confirmer = models.ForeignKey('Brewer', related_name='confirmer', on_delete=models.DO_NOTHING)
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)

    class Meta:
        verbose_name = ("entryflag")
        verbose_name_plural = ("entryflags")

