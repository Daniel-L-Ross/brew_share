"""View module for handling request about entries"""
import datetime
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from brew_shareapi.models import ( Entry, Brewer, Coffee,
                                    BrewMethod, FavoriteEntry, EntryReport,
                                    EntryStep)
from brew_shareapi.serializers import (EntryListSerializer, EntryDetailSerializer)
from brew_shareapi.image_handler import base64_image_handler
import cloudinary
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import cloudinary
import environ
env = environ.Env()
environ.Env.read_env()

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
        entries = Entry.objects.annotate(
            favorite=Count('favoriteentry', filter=Q(favoriteentry__brewer__user=request.auth.user))
        ).filter(private=False, block=False).order_by("date")

        username = self.request.query_params.get('username', None)
        favorite = self.request.query_params.get('favorite', None)
        coffee = self.request.query_params.get('coffee', None)
        method = self.request.query_params.get('method', None)
        searchterm = self.request.query_params.get('searchterm', None)

        if username is not None:
            if username == request.auth.user.username:
                brewer = Brewer.objects.get(user=request.auth.user)
                entries = brewer.entries.all()
            else:
                entries = entries.filter(brewer__user__username=username)

        if favorite is not None:
            entries = entries.filter(favorite=1)

        if coffee is not None:
            entries = entries.filter(coffee_id=coffee)
        
        if method is not None:
            entries = entries.filter(method_id=method)

        if searchterm is not None:
            # search entry fields (title, setup, tasting notes, setup)
            entries = entries.filter(
                Q(title__icontains=searchterm) | Q(setup__icontains=searchterm) | Q(tasting_notes__icontains=searchterm))
        
        serializer = EntryListSerializer(
            entries, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET request for single entry"""
        brewer = Brewer.objects.get(user=request.auth.user)
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

            try:
                FavoriteEntry.objects.get(entry=entry, brewer=brewer)
                entry.favorite = True
            except FavoriteEntry.DoesNotExist:
                entry.favorite = False

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
                return Response({}, status=status.HTTP_201_CREATED)
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
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            except Entry.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
            except FavoriteEntry.DoesNotExist as ex:
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
            try:
                brewer = Brewer.objects.get(user=request.auth.user)
                entry = Entry.objects.get(pk=pk, brewer=brewer)
                entry.private = not entry.private
                entry.save()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            except Entry.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post', 'put', 'delete'], detail=True)
    def steps(self, request, pk=None):
        """
        Handle creating, updating, and deleting steps for an entry
        """
        if request.method=="POST":
            brewer = Brewer.objects.get(user=request.auth.user)
            entry = Entry.objects.get(pk=pk, brewer=brewer)
            try:
                new_step = EntryStep()
                new_step.entry = entry
                new_step.descriptor = request.data["descriptor"]
                new_step.instruction = request.data["instruction"]
                new_step.seconds = request.data["seconds"]

                if request.data['stepImage']:
                        cloudinary.config(cloud_name = 'brewshare',
                            api_key = env("CLOUDINARY_API_KEY"),
                            api_secret = env("CLOUDINARY_SECRET_KEY"))
                        upload_pic = cloudinary.uploader.upload(request.data["stepImage"], folder='stepsFolder')
                        new_step.step_image = upload_pic['url']
                        new_step.cloudinary_image_id = upload_pic['public_id']
                else:
                    new_step.step_image = ""
                try:
                    new_step.clean_fields()
                except ValidationError as ex:
                    return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                new_step.save()
            
                return Response(status=status.HTTP_201_CREATED)
            except Entry.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        if request.method=="PUT":
            try: 
                step = EntryStep.objects.get(entry__brewer__user=request.auth.user, pk=int(request.data["id"]))

                step.descriptor = request.data["descriptor"]
                step.instruction = request.data["instruction"]
                step.seconds = request.data["seconds"]
                try:
                    # TODO: add cloudinary logic
                    image_data = base64_image_handler(request.data["stepImage"], step.instruction)
                    step.step_image = image_data
                except:
                    pass
                step.save()

                return Response(status=status.HTTP_204_NO_CONTENT)

            except EntryStep.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if request.method=="DELETE":
            try: 
                step = EntryStep.objects.get(entry__brewer__user=request.auth.user, pk=int(request.data["id"]))
                # TODO: add cloudinary logic
                step.delete()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

            except EntryStep.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status/status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)