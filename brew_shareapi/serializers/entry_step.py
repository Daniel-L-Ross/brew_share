from rest_framework import serializers
from brew_shareapi.models import EntryStep

class StepSerializer(serializers.ModelSerializer):
    """JSON Serializer for entry steps"""
    class Meta:
        model = EntryStep
        fields = ('id', 'step_image', 'descriptor', 'instruction', 'seconds', )