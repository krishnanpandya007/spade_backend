
from rest_framework import serializers
from spado_ubuntu.models import Account

class EditProfilePictureSerializer(serializers.ModelSerializer):

    # author_username= serializers.ReadOnlyField(source='author.user_name.username')

    # author_profilepic = serializers.ReadOnlyField(source='author.profile_pic if author.profile_pic else "Anonymous"')

    # likes = serializers.SlugRelatedField(queryset=User.objects.all(), many=True, slug_field="username")
    

    class Meta:
        model = Account
        fields = ['user_name','profile_pic']
