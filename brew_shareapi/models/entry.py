from brew_shareapi.models.entry_step import EntryStep
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Entry(models.Model):
    brewer = models.ForeignKey('Brewer', on_delete=models.CASCADE, related_name="entries")
    coffee = models.ForeignKey("Coffee", on_delete=models.DO_NOTHING)
    method = models.ForeignKey("BrewMethod", on_delete=models.DO_NOTHING)
    grind_size = models.CharField(max_length=25)
    coffee_amount = models.IntegerField()
    title = models.CharField(max_length=50)
    tasting_notes = models.CharField(max_length=50, blank=True)
    review = models.CharField(max_length=255, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],)
    setup = models.CharField(max_length=255)
    date = models.DateField()
    water_temp = models.IntegerField()
    water_volume = models.IntegerField()
    private = models.BooleanField()
    block = models.BooleanField()
    recipe = models.BooleanField()
    recommend = models.BooleanField()

    @property
    def steps(self):
        """property to return all steps on an entry"""
        all_steps = EntryStep.objects.filter(entry=self).order_by("seconds")

        return all_steps
        
    class Meta:
        verbose_name_plural = 'entries'

    @property
    def edit_allowed(self):
        """property to return boolean for conditional rendering on client side of edit and delete"""
        return self.__edit_allowed

    @edit_allowed.setter
    def edit_allowed(self, value):
        self.__edit_allowed = value

    @property
    def favorite(self):
        """property to return boolean for conditional rendering on client side for favorites"""
        return self.__favorite

    @favorite.setter
    def favorite(self, value):
        self.__favorite = value