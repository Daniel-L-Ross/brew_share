from rest_framework import serializers
from brew_shareapi.models import Entry

class EntrySerializer(serializers.ModelSerializer):
    """JSON serializer for products"""
    class Meta:
        model = Entry
        fields = ('id', 'title', 'date', 'user',
                    'coffee', 'grind_size', 'method', 'rating',
                    'tasting_notes', 'review', 'setup', 'water_temp',
                    'water_volume', 'recipe', 'recommend', )
        depth = 1