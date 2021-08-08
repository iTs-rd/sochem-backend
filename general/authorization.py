from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import ForumPost, ForumComment, ForumReply, Events, UserExtension


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def auth(request):
    CLIENT_ID = '210191010491-arcear3sgs4vbght2tke3ut0bo89566n.apps.googleusercontent.com'
    token = request.data['token']
    try:
        final = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    except ValueError:
        return Response({'error': "Wrong Token"}, status=status.HTTP_400_BAD_REQUEST)
    email = final.get('email', '')
    try:
        usr = User.objects.get(email__exact=email)
        usr.first_name = final.get('given_name', '')
        usr.last_name = final.get('family_name', '')
        usr.save()
        user_profile = UserExtension.objects.get(user=usr)
        # This is done to improve the photo quality from s96 to s 400.
        profile_photo_url = final.get('picture')
        index_s96 = profile_photo_url.find('s96')
        updated_profile_photo_url = profile_photo_url[:index_s96] + "s400" + profile_photo_url[index_s96+3:]
        user_profile.profile_photo = updated_profile_photo_url
        user_profile.save()
        token_value, _ = Token.objects.get_or_create(user=usr)
        final_token = str(token_value)
        return Response({'token': final_token}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        parts = email.split('@')
        if parts[1] == "iitbhu.ac.in" or parts[1] == "itbhu.ac.in":
            pass
        else:
            return Response({'error': "Wrong email used, login with @itbhu.ac.in only!"}, status=status.HTTP_400_BAD_REQUEST)
        new = User()
        new.email = email
        new.username = parts[0]
        new.first_name = final.get('given_name', '')
        new.last_name = final.get('family_name', '')
        new.set_unusable_password()
        new.is_staff = False
        new.is_superuser = False
        new.is_active = True
        new.save()
        Token.objects.create(user=new)
        token_value, _ = Token.objects.get_or_create(user=new)
        user_profile = UserExtension()
        user_profile.user = new
        user_profile.bio = ''
        user_profile.batch = parts[0].split('.')[-1]
        # This is done to improve the photo quality from s96 to s 400.
        profile_photo_url = final.get('picture')
        index_s96 = profile_photo_url.find('s96')
        updated_profile_photo_url = profile_photo_url[:index_s96] + "s400" + profile_photo_url[index_s96+3:]
        user_profile.profile_photo = updated_profile_photo_url
        user_profile.bio = "No Bio Added"
        user_profile.save()
        final_token = str(token_value)
        return Response({'token': final_token}, status=status.HTTP_200_OK)
