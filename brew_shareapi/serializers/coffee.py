from rest_framework import serializers
from brew_shareapi.models import Coffee

class CoffeeListSerializer(serializers.ModelSerializer):
    """JSON serializer for coffees"""
    class Meta:
        model = Coffee
        fields = ('id', 'roaster', 'name')

class CoffeeDetailSerializer(serializers.ModelSerializer):
    """JSON serializer for coffees"""
    class Meta:
        model = Coffee
        fields = ('id', 'roaster', 'name', 'country',
                    'region', 'process', 'recommended_method', 'website', 
                    )