from brew_shareapi.models.entry_step import EntryStep
from brew_shareapi.models.entry_flag import EntryFlag
from django.contrib import admin
from .models import (BrewMethod, Brewer, Coffee,
                    EntryFlag, EntryStep, Entry,
                    FavoriteEntry, RecipeReview, RecommendRecipe)
# Register your models here.

admin.site.register(BrewMethod)
admin.site.register(Brewer)
admin.site.register(Coffee)
admin.site.register(EntryFlag)
admin.site.register(EntryStep)
admin.site.register(Entry)
admin.site.register(FavoriteEntry)
admin.site.register(RecipeReview)
admin.site.register(RecommendRecipe)
