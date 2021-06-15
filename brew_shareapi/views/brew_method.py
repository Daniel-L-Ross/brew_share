"""View module for handling requests on brew methods"""
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from brew_shareapi.models import BrewMethod, Brewer
from brew_shareapi.serializers import MethodSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class BrewMethodView(ViewSet):
    """Request handlers for Brew Methods on the brew_share app"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized method instance
        """
        new_method = BrewMethod()
        new_method.brewer = Brewer.objects.get(user=request.auth.user)
        new_method.website = request.data["website"]
        new_method.name = request.data["name"]


        new_method.save()