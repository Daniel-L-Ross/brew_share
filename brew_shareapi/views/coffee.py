"""View module for handling requests on coffees"""
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from brew_shareapi.models import Coffee, Brewer
from brew_shareapi.serializers import CoffeeListSerializer, CoffeeDetailSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class CoffeeView(ViewSet):
    """Request handlers for coffees on the brew_share app"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized method instance
        """
        new_coffee = Coffee()
        new_coffee.brewer = Brewer.objects.get(user=request.auth.user)
        new_coffee.coffee_image = request.data["CoffeeImage"]
        new_coffee.roaster = request.data["roaster"]
        new_coffee.website = request.data["website"]
        new_coffee.name = request.data["name"]
        new_coffee.country = request.data["country"]
        new_coffee.region = request.data["region"]
        new_coffee.process = request.data["process"]
        new_coffee.recommended_method = request.data["recommendedMethod"]
        new_coffee.tasting_notes = request.data["tastingNotes"]

        try:
            new_coffee.clean_fields()
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        new_coffee.save()

        serializer = CoffeeDetailSerializer(
            new_coffee, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        """Handle GET operations
        Returns:
            Response -- JSON serialized list of coffees
        """
        coffees = Coffee.objects.all().order_by("name")

        serializer = CoffeeListSerializer(
        coffees, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET request for single method"""
        try:
            method = Coffee.objects.get(pk=pk)
            serializer = CoffeeDetailSerializer(method, context={'request': request})
            return Response(serializer.data)
        except Coffee.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT request for a method"""
        brewer = Brewer.objects.get(user=request.auth.user)
        try:
            if brewer.is_admin:
                coffee = Coffee.objects.get(pk=pk)
            else:
                coffee = Coffee.objects.get(pk=pk, brewer=brewer)

            coffee.coffee_image = request.data["CoffeeImage"]
            coffee.roaster = request.data["roaster"]
            coffee.website = request.data["website"]
            coffee.name = request.data["name"]
            coffee.country = request.data["country"]
            coffee.region = request.data["region"]
            coffee.process = request.data["process"]
            coffee.recommended_method = request.data["recommendedMethod"]
            coffee.tasting_notes = request.data["tastingNotes"]
            coffee.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Coffee.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for brew methods"""
        brewer = Brewer.objects.get(user=request.auth.user)
        try:
            if brewer.is_admin:
                coffee = Coffee.objects.get(pk=pk)
            else:
                coffee = Coffee.objects.get(pk=pk, brewer=brewer)
            coffee.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Coffee.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)