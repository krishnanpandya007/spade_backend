# from django.shortcuts import render

import re
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from api.forms import CreatePostForm
# from requests.models import Response
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from spado_ubuntu.communicator import predict_post_by_trend
from spado_ubuntu.models import Account, Comment, Post
from spado_ubuntu.serializers import PostSerializer
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from rest_framework.decorators import api_view, parser_classes

from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import MultiPartParser, FormParser
from user_profile.forms import EditProfilePicForm


# Create your views here.

'''
NOTE: Below all views, user needs to be authenticated
    -> For Degbugging (dev.) mode i am taking (authenticating user through API)
'''


class EditUsername(APIView):

    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, format=None):

        '''
        FORMAT:
        {
            'new_username': 'newUsername',
            'past_username': 'pastUsername'
        } 
        '''


        try:
            # Get the user 
            past_username = request.data.get('past_username')
            new_username = request.data.get('new_username')

            user = User.objects.get(username=past_username)


        except Exception as e:
            print("Error: While re-naming username: ", e)
            return Response({"error" : "Can't rename your username!"}, status=400)

        try:

            user.username = new_username
            user.save()
        except Exception as e:
            print("Error: While re-naming username: ", e)
            return Response({"error" : "Can't rename your username!"}, status=500)


        return Response({"success" : "Successfully, renamed the username!"}, status=200)
        

class EditName(APIView):

    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, format=None):

        '''
        FORMAT:
        {
            'new_name': 'newUsername',
            'past_username': 'pastUsername'
        } 
        '''

        try:
            # Get the user 

            past_username = request.data.get('past_username')
            first_name, last_name = request.data.get('new_name').split()

            user = User.objects.get(username=past_username)


        except Exception as e:
            print("Error: While re-naming username: ", e)
            return Response({"error" : "Can't rename your name!"}, status=400)

        try:

            user.first_name = first_name
            user.last_name = last_name

            user.save()
        except Exception as e:
            print("Error: While re-naming username: ", e)
            return Response({"error" : "Can't rename your name!"}, status=500)


        return Response({"success" : "Successfully, renamed the name!"}, status=200)
        

class EditEmail(APIView):

    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, format=None):

        '''
        FORMAT:
        {
            'new_email': 'newEmail',
            'past_username': 'pastUsername'
        } 
        '''


        try:
            # Get the user 
            past_username = request.data.get('past_username')
            new_email = request.data.get('new_email')

            user = User.objects.get(username=past_username)


        except Exception as e:
            print("Error: While re-naming username: ", e)
            return Response({"error" : "Can't reset your email!"}, status=400)

        try:

            user.email = new_email
            user.save()
        except Exception as e:
            print("Error: While re-naming username: ", e)
            return Response({"error" : "Can't reset your email!"}, status=500)


        return Response({"success" : "Successfully, reset the email!"}, status=200)


class EditUsername(APIView):

    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, format=None):

        '''
        FORMAT:
        {
            'new_username': 'newUsername',
            'past_username': 'pastUsername'
        } 
        '''


        try:
            # Get the user 
            past_username = request.data.get('past_username')
            new_username = request.data.get('new_username')

            user = User.objects.get(username=past_username)


        except Exception as e:
            print("Error: While re-naming username: ", e)
            return Response({"error" : "Can't rename your username!"}, status=400)

        try:

            user.username = new_username
            user.save()
        except Exception as e:
            print("Error: While re-naming username: ", e)
            return Response({"error" : "Can't rename your username!"}, status=500)


        return Response({"success" : "Successfully, renamed the username!"}, status=200)


class EditStatus(APIView):

    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, format=None):

        '''
        FORMAT:
        {
            'new_status': 'newStatus',
            'past_username': 'pastUsername'
        } 
        '''


        try:
            # Get the user 
            past_username = request.data.get('past_username')
            new_status = request.data.get('new_status')

            user = User.objects.get(username=past_username)
            account = Account.objects.get(user_name=user)

            assert new_status.capitalize() in ('Learning', 'Lazy', 'Working', 'Chilling', 'Spading'), "Invalid Status FOUND"

        except Exception as e:
            print("Error: While re-naming username: ", e)
            return Response({"error" : "Can't reset your status! Invlid Status or username"}, status=400)

        try:


            account.status = new_status
            account.save()
        except Exception as e:
            print("Error: While re-naming username: ", e)
            return Response({"error" : "Can't reset your status!"}, status=500)


        return Response({"success" : "Successfully, resseted the status!"}, status=200)


class EditStatusIndicator(APIView):

    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, format=None):

        '''
        FORMAT:
        {
            'new_statusIndicator': 'newStatusIndicator',
            'past_username': 'pastUsername'
        } 
        '''


        try:
            # Get the user 
            past_username = request.data.get('past_username')
            print("PAST USERNAME :", past_username)
            new_statusIndicator = request.data.get('new_statusIndicator')

            user = User.objects.get(username='k_a_p')
            account = Account.objects.get(user_name=user)

            assert new_statusIndicator.capitalize() in ('Do not disturb', 'Available', 'Busy', 'Away', 'Offline'), "Invalid Status Indicator FOUND"

        except Exception as e:
            print("Error: While re-naming username: ", e)
            return Response({"error" : "Can't reset your status Indicator! Invlid Status Indicator or username"}, status=400)

        try:


            account.status_indicator = new_statusIndicator.capitalize()
            account.save()
        except Exception as e:
            print("Error: While re-naming Status Indicator: 2", e)
            return Response({"error" : "Can't reset your status Indicator!"}, status=500)


        return Response({"success" : "Successfully, resseted the status Indicator!"}, status=200)


class EditBio(APIView):


    # REMAINING (CKEDITOR OR PLAIN TEXT(check kro pela))


    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, format=None):

        '''
        FORMAT:
        {
            'new_bio': 'newBio',
            'past_username': 'pastUsername'
        } 
        '''


        try:
            # Get the user 
            past_username = request.data.get('past_username')
            new_bio = request.data.get('new_bio')

            user = User.objects.get(username=past_username)
            account = Account.objects.get(user_name=user)

        except Exception as e:
            print("Error: While re-naming user bio: ", e)
            return Response({"error" : "Can't reset your Bio! Invlid Action or username"}, status=400)

        try:


            account.bio = new_bio
            account.save()
        except Exception as e:
            print("Error: While re-naming Status Indicator: ", e)
            return Response({"error" : "Can't reset your bio!"}, status=500)


        return Response({"success" : "Successfully, resseted the bio!"}, status=200)


class EditProfilepic(APIView):




    # Remaining To How to take Profile PIC




    parser_classes = (FormParser,MultiPartParser)
    renderer_classes = (JSONRenderer,)

    def post(self, request, format=None):

        '''
        FORMAT:
        {
            'new_profilePic': 'newProfilePic',
            'past_username': 'pastUsername'
        } 
        '''


        try:
            # Get the user 
            # past_username = request.data.get('past_username')
            # new_profilePic = request.data.get('new_profilePic')

            # user = User.objects.get(username=past_username)
            # account = Account.objects.get(user_name=request.user)
            account = get_object_or_404(Account, user_name=User.objects.get(username='jevik_pandya'))

            account.profile_pic = self.request.data['profile_pic']
            account.save()
            # reset_pic_form = EditProfilePicForm(request.POST or None, request.FILES or None, instance=account)

            # for field in reset_pic_form:
            #     print("Name: ", field.name ," Error: ", field.errors)





            # # Try using serializers instead of Forms



            # if (reset_pic_form.is_valid()):
            #     # reset_pic_form.save(commit=False)
            #     # reset_pic_form.user_name = request.user.pk
            #     print(request.user)
            #     obj = reset_pic_form.save(commit=False)
            #     obj.save()
            # else:
            #     print("Invalid Profile Pic FOUND")
            
            return Response({"success" : "Successfully reset your Profile Pic!"}, status=200)

        except Exception as e:
            print("Error: While re-naming user bio: ", e)
            return Response({"error" : "Can't reset your Profile Pic! Invlid Profile Pic or username"}, status=400)


class ResetPassword(APIView):

    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, format=None):

        '''
        FORMAT:
        {
            'old_password': 'new_password',
            'new_password': 'new_password',

            'past_username': 'pastUsername'
        } 
        '''


        try:
            # Get the user 
            past_username = request.data.get('past_username')
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            print(past_username)
            user = User.objects.get(username=past_username)

            assert user.check_password(old_password), "Old Password seems Different!"
        except Exception as e:
            print("Error: While re-naming user bio: ", e)
            return Response({"error" : "Can't reset your Password! Invlid Old Password or username"}, status=400)

        try:

            user.set_password(new_password)
            user.save()

        except Exception as e:
            print("Error: While re-naming Status Indicator: ", e)
            return Response({"error" : "Can't reset your password!"}, status=500)


        return Response({"success" : "Successfully, resseted the password!"}, status=200)
