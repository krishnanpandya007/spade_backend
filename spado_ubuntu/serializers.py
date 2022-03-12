# from xml.etree.ElementTree import Comment

from asyncore import read
from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import Account, Post, Comment
from django.contrib.auth.models import User

# from taggit_serializer.serializers import (TagListSerializerField,
#                                            TaggitSerializer)


# from serializers import TagListSerializerField
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
# from rest_framework.serializers import TagListSerializerFields
#Creating serializers from models what we built

class CommentSerializer(serializers.ModelSerializer):

    author_username= serializers.ReadOnlyField(source='author.user_name.username')

    author_profilepic = serializers.ReadOnlyField(source='author.profile_pic if author.profile_pic else "Anonymous"')

    likes = serializers.SlugRelatedField(queryset=User.objects.all(), many=True, slug_field="username")
    

    class Meta:
        model = Comment
        fields = ['id','author_username', 'descr', 'likes', 'time_since', 'author_profilepic']


class PostSerializer(serializers.ModelSerializer):

    tags = TagListSerializerField()

    author_name= serializers.ReadOnlyField(source='author.user_name.username')

    profile_pic = serializers.ReadOnlyField(source='author.profile_pic.url if author.profile_pic else "Anonymous"')

    first_name = serializers.ReadOnlyField(source='author.user_name.first_name')

    last_name = serializers.ReadOnlyField(source='author.user_name.last_name')

    likes = serializers.SlugRelatedField(queryset=User.objects.all(), many=True, slug_field="username")

    dislikes = serializers.SlugRelatedField(queryset=User.objects.all(), many=True, slug_field="username")

    comments = CommentSerializer(many=True, read_only=True)


    class Meta:
        model = Post
        fields = ['id','author_name', 'tags', 'title', 'descr', 'likes', 'dislikes', 'image_1', 'image_2', 'image_3', 'image_4', 'time_since','profile_pic', 'first_name', 'last_name', 'comments']

    
class AccountSerializer(serializers.ModelSerializer):

    username = serializers.ReadOnlyField(source='user_name.username')
    first_name = serializers.ReadOnlyField(source='user_name.first_name')
    last_name = serializers.ReadOnlyField(source='user_name.last_name')
    email = serializers.ReadOnlyField(source='user_name.email')
    
    created_posts = PostSerializer(many=True, read_only=True, source="get_posts")

    class Meta:

        model = Account

        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile_pic', 'status', 'status_indicator', 'status', 'bio', 'community', 'created_posts']


class SearchResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title'] 

