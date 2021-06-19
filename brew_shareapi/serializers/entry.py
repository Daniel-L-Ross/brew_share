from brew_shareapi.serializers.entry_step import StepSerializer
from rest_framework import serializers
from brew_shareapi.models import Entry
from brew_shareapi.serializers import (CoffeeListSerializer, CoffeeDetailSerializer, MethodSerializer,
                                        BrewerListSerializer, StepSerializer)

class EntryDetailSerializer(serializers.ModelSerializer):
    """JSON serializer for products"""
    coffee = CoffeeListSerializer(many=False)
    method = MethodSerializer(many=False)
    brewer = BrewerListSerializer(many=False)
    steps = StepSerializer(many=True)

    class Meta:
        model = Entry
        fields = ('id', 'title', 'date', 'brewer',
                    'coffee', 'grind_size', 'coffee_amount', 'method',
                    'rating', 'tasting_notes', 'review', 'setup',
                    'water_temp','water_volume', 'recipe', 'recommend', 'steps', 'private', 'edit_allowed')

class EntryListSerializer(serializers.ModelSerializer):
    """JSON serializer for products"""
    coffee = CoffeeListSerializer(many=False)
    method = MethodSerializer(many=False)
    brewer = BrewerListSerializer(many=False)

    class Meta:
        model = Entry
        fields = ('id', 'title', 'brewer',
                    'coffee', 'method',)