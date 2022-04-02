from os import stat
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.parsers import JSONParser
from rest_framework import status

from django.contrib.auth.models import User
from spado_ubuntu.models import Account

from account.serializers import UserSerializer

import re

from spado_ubuntu.serializers import AccountSerializer


class RegisterView(APIView):

    parser_classes = (JSONParser,)
    

    def post(self, req):

        try:

            print(req.data)

            data = req.data
    

            username = data["username"]
            email = data["email"]
            re_password = data["re_password"]
            password = data["password"]
            first_name = data["first_name"]
            last_name = data["last_name"]


            '''
            Username validation
            '''

            if (username):
                if (8 <= len(username) <=20):

                    username_regex = r'^(?=[a-zA-Z0-9._]{8,15}$)(?!.*[_.]{2})[^_.].*[^_.]$'
                    print('here')
                    if not (re.fullmatch(username_regex,username)):
                        print('here2')
                        return Response({"error": "username can only have '_', '.' at anywhere between with characters and numbers"})
                else:
                    return Response({"error": "Username may have minimum 8, maximum 15 characters"})
            else:
                return Response({"error": "Please provide username"}, status=400)


            '''
            Email Validation
            '''

            if email:

                email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

                if not re.fullmatch(email_regex, email):
                    # Invalid Email
                    return Response({"error": "Please enter valid email"}, status=400)
            else:
                return Response({"error": "Email must be provided"}, status=400)

            '''
            Password Validation & Creating User
            '''

            if(len(password) >= 8):

                if (password == re_password):

                    # 1. Creating User

                    try:
                        print("Creating...")
                        new_user = User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
                        print("Creted, Saving...")
                        new_user.save()
                        print("Saved")
                        return Response({"success": "Account successfully created!"}, status=201)

                    except Exception as e:
                        return Response({"error": "Can't able to add your account"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    # 2. Creating Account

                    '''
                    Not Creating as we dont have default images functionality
                    '''

                    # try:
                    #     new_user = Account.objects.create(user_name=new_user, auth_token="safiuhwh9w8hf98whwgf9")
                    #     new_user.save()

                    # except Exception as e:
                    #     return Response({"error": "Can't able to add your account"}, status=HTTP_500_INTERNAL_SERVER_ERROR)

                else:
                    return Response({"error": "Passwords do not match"}, status=400)
            else:
                return Response({"error": "password must be atleast 8 characters"}, status=400)

        except Exception as e:
            print(e)
            return Response({"error": "Something went wrong while creating account"}, status=400)


class GetUserDetailsView(APIView):
    permission_classes = (IsAuthenticated, )


    def get(self, request, format=None):

        try:
            
            account = Account.objects.get(user_name=request.user)

            account_serializer = AccountSerializer(account)

            return Response(account_serializer.data, status=status.HTTP_200_OK)
            # else:
            #     print("Error: ", user_serializer.errors)
            #     return Response({"user": " ".join(user_serializer.errors)}, status=415)
        except Exception as e:
            print("Can't get user data", e)
            return Response({"error": "can't access user"}, status=400)

class LoadProfileView(APIView):

    def post(self, request, format=None):

        try:

            username = request.data.get('username')

            print("Username: ", username)
            
            account = Account.objects.get(user_name=User.objects.get(username=username))

            account_serializer = AccountSerializer(account)

            return Response(account_serializer.data, status=status.HTTP_200_OK)
            # else:
            #     print("Error: ", user_serializer.errors)
            #     return Response({"user": " ".join(user_serializer.errors)}, status=415)
        except Exception as e:
            print("Can't get user data", e)
            return Response({"error": "can't access user"}, status=400)



class AdminUserInfo(APIView):

    permission_classes = (IsAdminUser,)

    def get(self, request):

        account = Account.objects.get(user_name=request.user)

        data = {
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'status': account.status,
            'status_indicator': account.status_indicator,
            'bio': account.bio,
            'profile_pic': account.profile_pic.url if account.profile_pic else False
        }

        return Response(data, status=200)
