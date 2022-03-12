from rest_framework import serializers
# from .models import Post
from spado_ubuntu.models import Post
#Creating serializers from models what we built

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'descr']

    
    