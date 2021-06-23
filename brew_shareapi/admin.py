from django.contrib import admin
from .models import (BrewMethod, Brewer, Coffee,
                    EntryReport, EntryStep, Entry,
                    FavoriteEntry, RecipeReview, RecommendRecipe)

# models registered for admin portal
admin.site.register(BrewMethod)
admin.site.register(Brewer)
admin.site.register(Coffee)
admin.site.register(EntryReport)
admin.site.register(EntryStep)
admin.site.register(Entry)
admin.site.register(FavoriteEntry)
admin.site.register(RecipeReview)
admin.site.register(RecommendRecipe)
