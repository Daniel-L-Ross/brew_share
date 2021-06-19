"""View module for handling request about entries"""
import datetime
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from brew_shareapi.models import ( Entry, Brewer, Coffee,
                                    BrewMethod, FavoriteEntry, EntryReport)
from brew_shareapi.serializers import (EntryListSerializer, EntryDetailSerializer)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class EntryView(ViewSet):
    """Request handlers for Entries on the brew_share app"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized entry instance
        """
        new_entry = Entry()
        new_entry.brewer = Brewer.objects.get(user=request.auth.user)
        new_entry.coffee = Coffee.objects.get(pk=int(request.data["coffee"]))
        new_entry.method = BrewMethod.objects.get(pk=int(request.data["method"]))
        new_entry.grind_size = request.data["grindSize"]
        new_entry.coffee_amount = int(request.data["coffeeAmount"])
        new_entry.title = request.data["title"]
        new_entry.date = datetime.date.today()
        new_entry.tasting_notes = request.data["tastingNotes"]
        new_entry.review = request.data["review"]
        new_entry.rating = int(request.data["rating"])
        new_entry.setup = request.data["setup"]
        new_entry.water_temp = int(request.data["waterTemp"])
        new_entry.water_volume = int(request.data["waterVolume"])
        new_entry.private = bool(request.data["private"])
        new_entry.block = False
        new_entry.recipe = False
        new_entry.recommend = False
        
        try:
            new_entry.clean_fields()
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        new_entry.save()

        serializer = EntryDetailSerializer(
            new_entry, context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        """Handle GET operations
        Returns:
            Response -- JSON serialized list of entries
        """
        user = request.auth.user
        brewer = Brewer.objects.get(user=user)

        entries = Entry.objects.all().order_by("date")

        user_id = request.query_params.get('user_id', None)
        if user_id == str(user.id):
            entries = entries.filter(brewer=brewer)
        else:
            entries = entries.filter(private=False).filter(block=False)


        serializer = EntryListSerializer(
            entries, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET request for single entry"""
        user = request.auth.user
        brewer = Brewer.objects.get(user=user)
        entry = Entry.objects.get(pk=pk)
        
        
        try:
            # return a post if the user owns it
            if entry.brewer == brewer:
                entry = entry
                entry.edit_allowed = True
            # admin can see blocked posts but not private posts
            elif brewer.is_admin and entry.private == False:
                entry = entry
                entry.edit_allowed = False
            # any user can view public, unblocked posts
            else:
                entry = Entry.objects.get(pk=pk, private=False, block=False)
                entry.edit_allowed = False
                
            serializer = EntryDetailSerializer(
                entry, many=False, context={'request': request}
            )
            return Response(serializer.data)
        
        except Entry.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle requests to update an entry"""
        try:
            brewer = Brewer.objects.get(user=request.auth.user)
            entry = Entry.objects.get(pk=pk, brewer=brewer)

            entry.coffee = Coffee.objects.get(pk=int(request.data["coffee"]))
            entry.method = BrewMethod.objects.get(pk=int(request.data["method"]))
            entry.grind_size = request.data["grindSize"]
            entry.coffee_amount = int(request.data["coffeeAmount"])
            entry.title = request.data["title"]
            entry.tasting_notes = request.data["tastingNotes"]
            entry.review = request.data["review"]
            entry.rating = int(request.data["rating"])
            entry.setup = request.data["setup"]
            entry.water_temp = int(request.data["waterTemp"])
            entry.water_volume = int(request.data["waterVolume"])
            entry.private = bool(request.data["private"])
            
            try:
                entry.clean_fields()
            except ValidationError as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            entry.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Entry.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for entries"""
        try:
            entry = Entry.objects.select_related('brewer').get(pk=pk, brewer__user=request.auth.user)
            entry.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Entry.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk=None):
        """Handle requests for favoriting an entry or removing the favorite"""

        if request.method == "POST":
            try:
                brewer = Brewer.objects.get(user=request.auth.user)
                entry = Entry.objects.get(pk=pk, private=False, block=False)
                
                try:
                    favorite = FavoriteEntry.objects.get(
                        brewer=brewer, entry=entry
                    )
                    return Response(
                    {'message': 'User already favorited this entry.'},
                    status=status.HTTP_204_NO_CONTENT
                    )
                except FavoriteEntry.DoesNotExist:
                    favorite = FavoriteEntry()
                    favorite.entry = entry
                    favorite.brewer = brewer
                    favorite.save()

            except Entry.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif request.method == "DELETE":
            try:
                brewer = Brewer.objects.get(user=request.auth.user)
                entry = Entry.objects.get(pk=pk)

                favorite = FavoriteEntry.objects.get(
                        brewer=brewer, entry=entry
                )
                favorite.delete()

            except Entry.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=True)
    def report(self, request, pk=None):
        """
        Report a post to create an entry_flag so an admin can review, 
        and decide if the content should be blocked.
        """
        if request.method == "POST":
            reporter = Brewer.objects.get(user=request.auth.user)
            entry = Entry.objects.get(pk=pk, block=False, private=False)
            try:
                report = EntryReport.get(reporter=reporter, entry=entry)
            except EntryReport.DoesNotExist:
                report = EntryReport()
                report.reporter = reporter
                report.entry = entry
                report.reason = request.data["reason"]
                report.save()
                return Response({}, status=status.HTTP_201_CREATED)
            except Entry.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=True)
    def private(self, request, pk=None):
        """
        Toggle privacy of a post by making a POST request to
        entries/pk/private
        """
        if request.method == "POST":
            brewer = Brewer.objects.get(user=request.auth.user)
            entry = Entry.objects.get(pk=pk, brewer=brewer)
            try:
                entry.private = not entry.private
                entry.save()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            except Entry.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @acrion(methods=['get'], detail=False) use ths to make an action without a pk