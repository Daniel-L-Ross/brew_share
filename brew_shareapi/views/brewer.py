"""View module for handling request about users"""
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from brew_shareapi.models import Brewer
from brew_shareapi.serializers import BrewerListSerializer, BrewerDetailSerializer
import cloudinary


class BrewerView(ViewSet):
    """Request handlers for users on the brew_share app"""

    def list(self, request):
        """
        Handle GET operations
        Returns:
            Response -- JSON serialized list of users/brewers
        """
        brewer = Brewer.objects.get(user=request.auth.user)
        try:
            if brewer.is_admin:
                brewers = Brewer.objects.all()

                serializer = BrewerListSerializer(
                    brewers, many=True, context={'request': request}
                )
                return Response(serializer.data)
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """Handle GET request for single brewer"""
        requester = Brewer.objects.get(user=request.auth.user)
        try:
            if requester.is_admin:
                brewer = Brewer.objects.get(pk=pk)
            else:
                brewer = Brewer.objects.get(pk=pk, user=requester)
            serializer = BrewerDetailSerializer(
                brewer, many=False, context={'request': request}
            )
            return Response(serializer.data)
        except Brewer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # TODO: if updated to allow all users to view, block non-admin from seeing banned users