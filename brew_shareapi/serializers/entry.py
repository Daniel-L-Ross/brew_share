from rest_framework import serializers
from brew_shareapi.models import Entry
from brew_shareapi.serializers import (CoffeeSerializer, MethodSerializer, BrewerSerializer)

class EntrySerializer(serializers.ModelSerializer):
    """JSON serializer for products"""
    coffee = CoffeeSerializer(many=False)
    method = MethodSerializer(many=False)
    brewer = BrewerSerializer(many=False)

    class Meta:
        model = Entry
        fields = ('id', 'title', 'date', 'brewer',
                    'coffee', 'grind_size', 'coffee_amount', 'method',
                    'rating', 'tasting_notes', 'review', 'setup',
                    'water_temp','water_volume', 'recipe', 'recommend', )