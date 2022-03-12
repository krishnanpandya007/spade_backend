from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
# from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Account, Post, Feedback, Issue
from .serializers import PostSerializer
from .forms import CreatePost
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from .communicator import predict_post_by_trend

# This is new comment

import requests
import uuid

# from spado_ubuntu import serializers 



class HomeStaffView(APIView):

    permission_classes = (IsAdminUser,)

    def get(self, request):
        return Response({"data": request.user.username}, status=200)

class HomeView(APIView):

    def get(self, request):
        # return render(request, 'index.html')
        # serializers_class = PostSerializer
        # queryset = Post.objects.all()
        # Show relevant posts by hackerrank(newer) or reddit(trending)(+) recommendations
        try:
            trending_post_ids = predict_post_for_userid(is_authenticated=request.user.is_authenticated, user_id=request.user.pk, catagory="trending")["post_ids"]

            trending_posts = Post.object.filter(pk__in=trending_post_ids)
            trending_posts_serializer = PostSerializer(trending_posts, many=True)

            # return Response({'posts': trending_posts_serializer, 'error': False})
            return render(request, 'index.html')

        except Exception as e:
            print("[FAILED]: Can't fetch data for recommend user_name: %s type: %s" % (request.user.username, "trending"))
            # return Response({'posts': {}, 'error': True})

            return render(request, 'index.html', context={'new':'how'})

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        
        user = authenticate(request, username=username, password=email)
        if user is not None:
            login(request, user)
            # return HttpResponse(f"<h1>{user.username}</h1>")
            return Response({'message': 'Logged In Successfully!', 'error': False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'No such username with that password exists!', 'error': True}, status=status.HTTP_200_OK)




@csrf_protect
@login_required
def create_post(response):
    if response.method == "GET":
        form = CreatePost()
        context = {
            'form':form
        }
        return render(response, 'create_post.html', context)
    elif response.method == "POST":
        form = CreatePost(response.POST, response.FILES)
        if form.is_valid:

            my_post = form.save(commit=False)

            # my_post.author = User.objects.get(username=response.user.username).username
            '''
            Below code: don't go on syntex just trying to save to build a class instance!
            '''
            print("CREATED_POST_USERNAME:",response.user.username )
            my_post.author = Account.objects.get(user_name=User.objects.get(username=response.user.username))
            # print("-------",type( User.objects.get(username=response.user.username)))
            # print(response.user)
            # print("User:", my_post.author)
            my_post.save()
            form.save_m2m()
            return redirect('home')

@api_view(['GET', 'POST'])
def submit_feedback(response):
    try:
        print(response.data)
        data = response.data
        user = User.objects.filter(username=response.user.username).first()
        print(user)
        issue = Issue.objects.create(problem=data['issue'])
        issue.save()

        if not Feedback.objects.filter(sent_by=user).exists():
            feedback = Feedback.objects.create(sent_by=user)
            feedback.experiance = data['experiance']
            feedback.issues.add(issue)

            feedback.save()
            return HttpResponse("Create feeda")

        else:

            feedback = Feedback.objects.filter(sent_by=user).first()
            feedback.experiance = data['experiance']
            # if not Issue.objects.filter(problem=data['issue']):
            feedback.issues.add(issue)


            feedback.save()
            return HttpResponse("Added feeda")


        # feedback.save()
        print("CREATED FEEDBACK")
    except Exception as e:
        return HttpResponse("SOME ERROR!")


# By this we are communicating with go-server(prediction)XcL9



# @csrf_protect 
@api_view(['GET','POST'])
def load_more_posts(response):
    """
    Options for filter_by:
        --> trending
        --> created_at
        --> most_relovant // Predicted By Server
    """
    return Response({'message': 'GOt Message!'}, status=status.HTTP_200_OK)
    if response.method == "POST":
        quantity = response.data["quantity"]
        filter_by = response.data["filter_by"]
        quantity = min([6, quantity])

        had_posts = response.data['had_posts']#Posts(id) client:for give them unique posts!
        print("quantity:", quantity, "Filter--BY:", filter_by)
    else:
        return HttpResponse("Oops Something went wrong!")
    if response.method == "POST":

        if filter_by == "trending":
            # Means Trending ones...
            # sorted_posts = Post.objects.annotate(q_count=Count('likes')).order_by('-q_count')
            predicted_post_ids = predict_post_for_userid(1, catagory=filter_by)
            sorted_posts = Post.objects.filter(pk__in=predicted_post_ids['post_ids'])
            print(sorted_posts)
            # Below line prevents us if we are showing the post to user on which they already have on screen!

            sorted_posts = [post for post in sorted_posts if post.id not in had_posts]

            print("New sorted posts", sorted_posts)
            sorted_posts = sorted_posts[:quantity] # we are taking top int(quantity) posts
            serializer_s = PostSerializer(sorted_posts, many=True)
            #In this for loop we appending tags, otherstuffs
            
            if sorted_posts:
                for ind, i in enumerate(serializer_s.data):
                    tags = [ tag_name.name for tag_name in list(Post.objects.get(title=serializer_s.data[ind]['title']).tags.all())]
                    # print("USERNAME:", i['author'])
                    author_user = User.objects.get(username='author_1') # CHANGE JUST DEBUGGING
                    i['error'] = ""
                    i['author'] = User.objects.get(pk=i['author']).username

                    # check(-)
                    i['created_on'] = Post.objects.get(pk=i['id']).time_since()
                    print("DONE FIRST PROB..", author_user)
                    user_profile = Account.objects.get(user_name=author_user)
                    i['tags'] = tags
                    i['user_profile'] = user_profile.profile_pic.url
                print(tags)
                print("GOTTED::DATA:", serializer_s.data[0]['created_on'])
                # return JsonResponse({"data":serializer.data}, status=200)
                return Response(serializer_s.data)
            else:
                return JsonResponse({'error':'no more posts'}, status=200)            

        elif filter_by == "recent":
            # sorted_posts = Post.objects.all()
            # sorted_posts = [post for post in sorted_posts if post.id not in had_posts][::-1]

            # Setting some fix max_age on created_on
            # Maximum max_age time = 1day (which posts are older than 1 day doesnt qualify for this)
            #Setting var(strict) why? -> (strict ? n(qualified_posts) <= n('quantity_posts') : n(qualified_posts) = n(quantity_posts))
            # Using Reddit Formula (lol we use all formulas xD) as it fits well in recent and trending session

            predicted_posts = predict_post_for_userid(1, catagory='recent', strict=False, max_age=1, duration_in='day') # we have less posts so no strict mode
            sorted_posts = Post.objects.filter(pk__notin=had_posts)

            print("New sorted posts", sorted_posts)
            sorted_posts = sorted_posts[:quantity]
            serializer_s = PostSerializer(sorted_posts, many=True)
            #In this for loop we appending tags, otherstuffs

            if sorted_posts:
                print("LEN_POSTS", len(sorted_posts)) # we are taking top int(quantity) posts
                for ind, i in enumerate(serializer_s.data):
                    tags = [ tag_name.name for tag_name in list(Post.objects.get(title=serializer_s.data[ind]['title']).tags.all())]
                    print("USERNAME:", i['author'])
                    author_user = User.objects.get(username=i['author'])
                    i['error'] = ""
                    i['author'] = User.objects.get(pk=i['author']).username
                    # check(-)
                    i['created_on'] = Post.objects.get(pk=i['id']).time_since()
                    print("DONE FIRST PROB..", author_user)
                    user_profile = Account.objects.get(user_name=author_user)
                    i['tags'] = tags
                    i['user_profile'] = user_profile.profile_pic.url
                print(tags)
                print("GOTTED::DATA:", serializer_s.data[0]['created_on'])
                # return JsonResponse({"data":serializer.data}, status=200)
                return Response(serializer_s.data)
            else:
                return JsonResponse({'error':'no more posts'}, status=200)            


            # return Response(serializer.data)
        elif filter_by == 'relevant':
            # has to be default choice!
            # Request for make more relevant post for user
            # To go-server

            user_id = 1
            print(f"***\n\n{user_id}\n\n***")
            predicted_posts: dict = predict_post_for_userid(23, catagory='relevant')
            # go_server_url = "http://localhost:8500"
            # res = requests.post(go_server_url, json={'user_id':})


            #after getting resonse we update the page as well
            # Sorting posts by(likes/created_on(sec.)) ratio
            sorted_posts = [i for i in Post.objects.all()] 
            # Use: not__in method direcly communicate to SQL;
            sorted_posts = sorted(sorted_posts, key=lambda x:((x.likes.count())/(int(x.created_on.strftime('%y%m%H%M%S')))))
            sorted_posts = [post for post in sorted_posts if post.id not in had_posts][::-1]

            print("New sorted posts", predicted_posts)
            sorted_posts = sorted_posts[:quantity] # we are taking top int(quantity) posts
            serializer_s = PostSerializer(sorted_posts, many=True)
            #In this for loop we appending tags, otherstuffs

            if sorted_posts:
                for ind, i in enumerate(serializer_s.data):
                    tags = [ tag_name.name for tag_name in list(Post.objects.get(title=serializer_s.data[ind]['title']).tags.all())]
                    print("USERNAME:", i['author'])
                    # author_user = User.objects.get(username=i['author'])
                    author_user = User.objects.first()
                    i['error'] = ""

                    # check(-)
                    i['created_on'] = Post.objects.get(pk=i['id']).time_since()
                    print("DONE FIRST PROB..", author_user)
                    user_profile = Account.objects.get(user_name=author_user)
                    i['tags'] = tags
                    i['user_profile'] = user_profile.profile_pic.url
                print(tags)
                print("GOTTED::DATA:", serializer_s.data[0]['created_on'])
                # return JsonResponse({"data":serializer.data}, status=200)
                return Response(serializer_s.data)
            else:
                return JsonResponse({'error':'no more posts'}, status=200)            

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        data = response.data
        print("recieved data:", data)
        security_pin = "IDUbbSIBDUBsiduiS6t763t6d6w7633"
        try:
            if data['like_token'] == security_pin:
                target_post = Post.objects.get(id=int(data['post_id']))
                if target_post:
                    if data['action'] == "+":
                        target_post.likes += 1
                        target_post.save()
                        # print("savedl")
                    elif data['action'] == "-":
                        target_post.likes -= 1
                        target_post.save()
            else:
                print("[SUSPICIOUS_REQ]{POST}:fetch_api_call --views.py if(2)^")
                pass
        except Exception as e:
            print("[REQUEST_ERROR]:at function --> fetch_api_call --views.py")
            pass
        return HttpResponse(response.data)


# ISSUE handle like isnt working preperly



def signup(response):
    if response.method == "POST":
        username = response.POST['user_name'] 
        email = response.POST['email'] 
        password = response.POST['password'] 
        tnc = response.POST['agreetnc']
        # Checking For validd user or not

        if User.objects.filter(username=username).first():
            print('*'*10, "user exists")
            context = {
                'user_exists':'f',
            }
            return render(response, 'signup.html', context)
        # if User.objects.filter(email=email).first():
        #     print('*'*10, "email exists")
        #     context = {
        #         'email_exists':'f',
        #     }
        #     return render(response, 'spado/signup.html', context)
        try:
            new_user = User.objects.create(username=username, email=email, password=password)
            auth_token = str(uuid.uuid4())
            user_account = Account.objects.create(user_name=new_user, auth_token=auth_token)
            print("created account of user!")
            print("pre caling func.")
            send_verification_mail(email, auth_token)
            user_account.save()
            print("after caling func.")
            # new_user = form.save(commit=False)
            # new_user.is_active = False
            new_user.save()
            return redirect('check_mail')
        except Exception as e:
            print('*'*10, e)
            context = {
                'internal_error':'t',
            }
            return render(response, 'signup.html', context)

    else:
        return render(response, "signup.html", {})

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                redirect('home')

    else:
        return render(request, 'loginform.html')
@api_view(['GET', 'POST'])
def trial(request):
    if request.method == "GET":
        return render(request, 'trial.html')
    else:
        print(request.data)
        return Response(request.data)

# Refresh the page once you verified your account
def check_mail(request):
    return render(request, 'check_mail.html')

def verify(request, auth_token):
    print("---------->Gone to Verified")
    #below thing has to be edited
    account = Account.objects.filter(auth_token=auth_token).first()
    try:
        if account:
            if account.is_valid:
                #Here user is already verified
                messages.success("Account Already verified!")
                return render(request, '/')
            else:
                account.is_valid = True
                account.save()
                
                return render(request, 'spado/loginform.html')
    except Exception:
        messages.error("something went wrong, Please try again!")
        return redirect('signup')
#     if request.method == "POST":
#         otp_code = request.POST['otpcode']
#         print("-->>>>>otp code: ", otp_code)
#         return HttpResponse("<h1>this IS DONE!</h1>")
#     else:
#         return render(request, 'spado/otpverification.html', {})

def send_verification_mail(email, authtoken):
    subject = "Verify your account"
    message = f"Hey there, Your account has to be varified please click on the link ahed to varify your account https://127.0.0.1/verify/{authtoken}"
    email_from = settings.EMAIL_HOST_USER
    reciever_list = [email]
    send_mail(subject, message, email_from, reciever_list, fail_silently=False)
    # eml = EmailMessage(subject, message, to=reciever_list)
    # eml.send()
    print("--->Sent verification link to", email)


