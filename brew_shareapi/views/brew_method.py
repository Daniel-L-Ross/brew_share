"""View module for handling requests on brew methods"""
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from brew_shareapi.models import BrewMethod, Brewer
from brew_shareapi.serializers import MethodSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from brew_shareapi.image_handler import base64_image_handler

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

        try:
            image_data = base64_image_handler(request.data["brewMethodImage"], new_method.name)
            new_method.method_image = image_data
        except:
            new_method.method_image = None

        try:
            new_method.clean_fields()
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        new_method.save()

        serializer = MethodSerializer(
            new_method, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        """Handle GET operations
        Returns:
            Response -- JSON serialized list of brew methods
        """
        methods = BrewMethod.objects.all().order_by("name")

        serializer = MethodSerializer(
        methods, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET request for single method"""
        try:
            method = BrewMethod.objects.get(pk=pk)
            serializer = MethodSerializer(method, context={'request': request})
            return Response(serializer.data)
        except BrewMethod.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT request for a method"""
        brewer = Brewer.objects.get(user=request.auth.user)
        try:
            if brewer.is_admin:
                method = BrewMethod.objects.get(pk=pk)
            else:
                method = BrewMethod.objects.get(pk=pk, brewer=brewer)
            method.method_image = request.data["brewMethodImage"]
            method.website = request.data["website"]
            method.name = request.data["name"]
            try:
                image_data = base64_image_handler(request.data["brewMethodImage"], method.name)
                method.method_image = image_data
            except:
                pass

            try:
                method.clean_fields()
            except ValidationError as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            method.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except BrewMethod.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for brew methods"""
        brewer = Brewer.objects.get(user=request.auth.user)
        try:
            if brewer.is_admin:
                method = BrewMethod.objects.get(pk=pk)
            else:
                method = BrewMethod.objects.get(pk=pk, brewer=brewer)
            method.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except BrewMethod.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)