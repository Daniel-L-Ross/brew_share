from rest_framework import serializers
from brew_shareapi.models import BrewMethod

class MethodSerializer(serializers.ModelSerializer):
    """JSON serializer for brew methods"""
    class Meta:
        model = BrewMethod
        fields = ('id', 'name','method_image', 'website', )