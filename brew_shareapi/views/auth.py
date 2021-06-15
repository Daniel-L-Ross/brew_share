from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from brew_shareapi.models import Brewer
import json

@csrf_exempt
def login_user(request):
    '''Handles the authentication of a brewer

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    if request.method == 'POST':

        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            brewer = Brewer.objects.get(user=authenticated_user)
            is_admin = brewer.is_admin
            brewer_id = brewer.id
            data = json.dumps({"valid": True, "token": token.key, "id": brewer_id, "isStaff": is_admin})
            return HttpResponse(data, content_type='application/json')

        else:
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')

@csrf_exempt
def register_user(request):
    '''Handles the creation of a new brewer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )

    brewer = Brewer.objects.create(
        bio=req_body['bio'],
        user=new_user,
        profile_image=req_body['profileImage'],
        is_admin = False, 
        current_coffee = req_body['currentCoffee'],
        current_brew_method = req_body['currentBrewMethod'],
        private = False
    )

    # Commit the user to the database by saving it
    brewer.save()

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)
    is_admin = brewer.is_admin
    brewer_id = brewer.id

    data = json.dumps({"valid": True, "token": token.key, "id": brewer_id, "isAdmin": is_admin})
    return HttpResponse(data, content_type='application/json')