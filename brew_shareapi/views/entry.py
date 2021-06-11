"""View module for handling request about entries"""
import datetime
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from brew_shareapi.models import ( Entry, Brewer, Coffee,
                                    BrewMethod)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class EntrySerializer(serializers.ModelSerializer):
    """JSON serializer for products"""
    class Meta:
        model = Entry
        fields = ('id', 'title', 'date', 'user',
                    'coffee', 'grind_size', 'method', 'rating',
                    'tasting_notes', 'review', 'setup', 'water_temp'
                    'water_volume', 'recipe', 'recommend', )

class Entries(ViewSet):
    """Request handlers for Entries on the brew_share app"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        new_entry = Entry()
        new_entry.user = Brewer.objects.get(user=request.auth.user)
        new_entry.coffee = Coffee.objects.get(pk=request.data["coffee"])
        new_entry.method = BrewMethod.objects.get(pk=request.data["method"])
        new_entry.grind_size = request.data["grindSize"]
        new_entry.title = request.data["title"]
        new_entry.date = datetime.date.today()
        new_entry.tasting_notes = request.data["tastingNotes"]
        new_entry.review = request.data["review"]
        new_entry.rating = request.data["rating"]
        new_entry.setup = request.data["setup"]
        new_entry.water_temp = request.data["waterTemp"]
        new_entry.water_volume = request.data["waterVolume"]
        new_entry.private = request.data["private"]
        new_entry.recipe = request.data["recipe"]
        new_entry.recommend = request.data["recommend"]
        
        try:
            new_entry.clean_fields()
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        new_entry.save()

        serializer = EntrySerializer(
            new_entry, context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list