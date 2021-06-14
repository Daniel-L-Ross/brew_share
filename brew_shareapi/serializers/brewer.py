from rest_framework import serializers
from django.contrib.auth.models import User
from brew_shareapi.models import Brewer

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for brewer's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', )

class BrewerSerializer(serializers.ModelSerializer):
    """JSON serializer for brewer extension of user model"""
    user = UserSerializer(many=False)

    class Meta:
        model = Brewer
        fields = ('user', )
        depth = 1