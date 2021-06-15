from django.db import models

class FavoriteEntry(models.Model):
    brewer = models.ForeignKey('Brewer', on_delete=models.CASCADE)
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("favoriteentry")
        verbose_name_plural = ("favoriteentries")

