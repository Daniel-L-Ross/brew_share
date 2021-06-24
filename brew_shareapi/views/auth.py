from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from brew_shareapi.models import Brewer
from brew_shareapi.image_handler import base64_image_handler
import json

@csrf_exempt
def login_user(request):
    '''Handles the authentication of a brewer

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    if request.method == 'POST':

        email = req_body['email']
        password = req_body['password']
        user = User.objects.get(email=email)
        username = user.username
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            brewer = Brewer.objects.get(user=authenticated_user)
            is_admin = brewer.is_admin

            data = json.dumps({"valid": True, "token": token.key, "isAdmin": is_admin, "username": username})
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

    # handle base64 image string for profile image
    try:
        image_data = base64_image_handler(req_body['profileImage'], new_user.id)
    except:
        image_data = None

    # save the brewer user extension
    brewer = Brewer.objects.create(
        bio=req_body['bio'],
        user=new_user,
        profile_image=image_data,
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
    username = new_user.username

    data = json.dumps({"valid": True, "token": token.key, "isAdmin": is_admin, "username": username})
    return HttpResponse(data, content_type='application/json')