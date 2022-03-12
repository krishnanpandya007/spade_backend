# import re
from ast import parse
import re
from unittest import result
from urllib import request
from django.contrib.auth.models import User
from django.shortcuts import render
from api.forms import CreatePostForm
# from requests.models import Response
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from spado_ubuntu.communicator import predict_post_by_trend
from spado_ubuntu.models import Account, Comment, Post
from spado_ubuntu.serializers import PostSerializer, SearchResultSerializer
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from rest_framework.decorators import api_view, parser_classes

from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import MultiPartParser, FormParser


from django.contrib.postgres.search import TrigramSimilarity
# Create your views here.
MAX_LOAD_MORE_POSTS_LIMIT = 6
class LoadMorePostsByRelevant(APIView):

    permission_classes = (IsAuthenticated,)

    # Default is by trned
    
    def get(self, response):
        try:
            quantity = min([MAX_LOAD_MORE_POSTS_LIMIT, response.data.get('quantity')]) 
            had_posts = response.data.get('had_posts')

            user_id = response.user.pk

            print("Predections (relevant) for UserId:%d " % (user_id))

            predicted_posts = predict_post_by_trend(is_authenticated=bool(user_id),user_id=user_id, catagory="relevant")

            if predicted_posts:
                predicted_posts = [post for post in predicted_posts if post not in had_posts]
                posts = Post.object.filter(pk__in=[predicted_posts])[:quantity]

                post_serializer = PostSerializer(posts, many=True)

                for ind, i in enumerate(post_serializer.data):
                    tags = [ tag_name.name for tag_name in list(Post.objects.get(title=post_serializer.data[ind]['title']).tags.all())]
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

                return Response(post_serializer.data, status=status.HTTP_200_OK)           
            else:
                return Response({"error": True, "message": "Error while loading relevant posts"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        except Exception as e:
            print("[FETCH_RELEVANT_POST_ERROR]: %s" % (e))


# def CreatePost(request):


class CreatePost(APIView):

    # permission_classes = (IsAuthenticated,)
    # serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, format=None):
        print("Made REQ.")
        print(hasattr(request, 'data'))
        print("DATA: ", request.__dict__)
        # print(request.data)

        # user = User.objects.get(username="jevik_pandya")

        # acc = Account.objects.get(user_name=user)

        # post_serializer = PostSerializer(Post.objects.all(), many=True)

        # post_serializer = PostSerializer(data=request.data['form'])
        # if post_serializer.is_valid():
        #     print("VALID SERIALIZER")
        #     post_serializer.save()
        #     return Response({'message': 'Done', status: status.HTTP_200_OK})

        # if post_serializer.is_valid():
            # post_serializer.save()
        print("ERROR")
        return Response({'message': 'ERR krishnan pandya'}, status=status.HTTP_201_CREATED) 
    

# class dummy_login(APIView):

#     parser_classes = (MultiPartParser, FormParser, JSONParser)

#     def put(self, req,format=None):

#         print(req.__dict__)
#         print(req.FILES.getlist('files'))

#         return Response({'error': False}, status=status.HTTP_200_OK)

from rest_framework.decorators import renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

@api_view(('POST',))
@parser_classes([JSONParser, MultiPartParser, FormParser])
def create_post(req, format=None, *args, **kwargs):
    print(req.user)

    print(f"{req.data = }\n{req.POST = }\n{req.FILES = }\n")

    form = CreatePostForm(req.POST)

    try:

        print('user: ', req.user) 
        user_account = Account.objects.get(user_name=req.user) 

    except Exception as e:

        return Response({"Error" : "Can't authenticate user!"}, status=500)

    for field in form:
        print("Name: ", field.name, " Error: ", field.errors)

    if form.is_valid() :

        
        obj = form.save(commit=False)
        obj.author = user_account
        # Initializations
        obj.save()

        
        form.save_m2m()
        print('saved')

    else:
        print('[FAILED]: unsuccessfull save attempt!')

    # except Exception as e:
    #     print("Can't Do this: ", e)

    return Response({'error': False}, status=status.HTTP_201_CREATED)

class CreateComment(APIView):

    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):


        try:

            comment_data = request.data['comment']
            username = request.data['username']
            post_id = request.data['post_id']
        
        except Exception as e:
            
            return Response({'error': 'Invalid pre-request found'}, status=400)

        comment_data = request.data['comment']
        username = request.data['username']
        post_id = request.data['post_id']

        try:

            user = User.objects.get(username=username)
        
        except Exception as e:

            return Response({'error': 'username invalid'}, status=400)



        try:

            print(username, comment_data)

            comment = Comment.objects.create(author=Account.objects.get(user_name=user), descr=comment_data)
            comment.save()
        
        except Exception as e:
            # print(e)
            
            return Response({'error': 'Can\'t create comment instance'}, status=400)

        try:

            post = Post.objects.get(pk=post_id)
            post.comments.add(comment)
            post.save()
        
        except Exception as e:
            
            return Response({'error': 'post_id invalid or can\'t able to save comment'}, status=400)
    

        return Response({'success': 'Comment added successfully'}, status=201)
        
            # print("username is invalid!")


class HandleActionComment(APIView):

    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):

        try:
            
            username = request.data.get('username')
            action = request.data.get('action')
            comment_id = request.data.get('comment_id')


        except Exception as e:
            print(e)
            return Response({'error': 'Can\'t retrieve valid data'}, status=400)

        
        try:
            
            user = User.objects.get(username=username)

        except Exception as e:
            print(e)
            return Response({'error': 'Invalid Username'}, status=400)

        
        try:
            
            comment = Comment.objects.get(pk=comment_id)

        except Exception as e:
            print(e)
            return Response({'error': 'Invalid comment Id'}, status=400)

        
        try:

            if(action == 'remove'):
                # Remove Like
                comment.likes.remove(user)
            else:
                # Add like
                comment.likes.add(user)           
                

        except Exception as e:
            print(e)
            return Response({'error': 'Can\'t perform instructed action'}, status=500)

        
        return Response({'success': 'Action Updated Successfully'}, status=200)


# class LoadPosts(APIView):

#     # URL: api/load_more_posts

#     # {quantity: 5-8, catagory: ['trending', 'relevant', 'most_liked', 'recent']}

#     parser_classes = (JSONParser,)
#     renderer_classes = (JSONRenderer,)

#     def post(self, request, format=None):

#         try:
#             quantity = request.data.get('quantity')
#             catagory = request.data.get('catagory')

#             # When user likes any post the score of that post is 0 as we try  to not show that again to user
#             posts = Post.objects.get(pk=1)
 

#             post_serializer.is_valid(raise_exception=True)

#             return Response(post_serializer.data, status=500)

#         except Exception as e:
#             print("REASON :::::   ", e)
#             return Response({'error': 'Invalid pre-requirments recieved!'}, status=400)
@api_view(['POST'])
def load_account_posts(request):
    try:
        quantity = int(request.data.get('quantity'))
        author = request.data.get('author')

        posts = Post.objects.filter(author__user_name__username=author)

        if (posts.exists()):
            post_serializer = PostSerializer(posts, many=True)
            return Response(post_serializer.data, status=200)


        return Response({'error': 'No posts found associated with this author.'}, status=404)
        
    except Exception as e:
        print("Invalid Formation Found!", e)
        return Response({'error': 'Invalid pre-requirments recieved!'}, status=400)



@api_view(['POST'])
def load_posts(request):

    try:
        quantity = int(request.data.get('quantity'))
        catagory = request.data.get('catagory')

        quantity = min(quantity, 6) # Setting max_load_post_limit to 6

        # assert catagory == 'trending'

        # When user likes any post the score of that post is 0 as we try  to not show that again to user

        # result = predict_post_for_userid(is_authenticated=False, user_id=1, catagory=catagory)
        result = predict_post_by_trend()

        print(result)

        if (result):
            

            posts = Post.objects.filter(pk__in=result[:quantity])
            print('before')
            post_serializer = PostSerializer(posts, many=True)
            print('After')

            print(post_serializer.data)


            return Response(post_serializer.data, status=200)
        
        else:
            posts = list(Post.objects.all())[:quantity]
            print('before')
            post_serializer = PostSerializer(posts, many=True)
            print('After')

            print(post_serializer.data)


            return Response(post_serializer.data, status=200)

    except Exception as e:
        print("REASON :::::   ", e)
        return Response({'error': 'Invalid pre-requirments recieved!'}, status=400)




class HandleActionPost(APIView):

    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):

        try:
            username:str = request.data.get('username')
            post_id:int = request.data.get('post_id') 
            choice:list = request.data.get('choice')  # Like/Dislike 
            action:list = request.data.get('action')  # Add/remove   
            print('Data: ', request.data, "\nPost: ", request.POST)
            target_post = Post.objects.filter(pk=post_id)
            user = User.objects.filter(username=username)

            if target_post.exists() and user.exists():
                target_post = target_post.first()
                user = user.first()
                if 'remove' in action:
                    remove_pos = action.index('remove')
                    if choice[remove_pos] == 'like':
                        # remove dislike
                        target_post.likes.remove(user)
                    else:
                        target_post.dislikes.remove(user)
                if 'add' in action:
                    add_pos  = action.index('add')
                    if choice[add_pos] == 'like':
                        # Add Like
                        target_post.likes.add(user)
                    else:
                        target_post.dislikes.add(user)
                        
                target_post.save()

                print('saved')

                return Response({'success': "Updated Action"}, status=200)

            return Response({'error': "Invalid username or post_id found"}, status=400)
            
                
            

        except Exception as e:
            print("Error While Handling Actions for post", e)
            return Response({'error': "Can't Update Actions"}, status=500)



# TRY to make funtional view any then serailize


@api_view(['POST'])
def get_post_by_search_text(request):
    try:
        search_query = request.data.get('search_query')
        n_posts = request.data.get('n_posts')
        n_posts = min(MAX_LOAD_MORE_POSTS_LIMIT, n_posts)

        query_set = Post.objects.all()

        print("DEBUG::QUERY-> ", search_query)

        filtered_posts = [post for post in query_set.annotate(similarity=TrigramSimilarity('title', search_query)).order_by('-similarity')][:n_posts+1]

        posts_serializer = SearchResultSerializer(filtered_posts, many=True)

        return Response(posts_serializer.data, status=200)

    except Exception as e:

        print("Can't fetch posts related to search_query: ", e)
        return Response({"error": "Can't fetch posts related to search_query"}, status=500)








