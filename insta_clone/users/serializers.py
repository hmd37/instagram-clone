from rest_framework import serializers

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='user-detail',  
        lookup_field='username'   
    )
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            'url', 'id', 'username', 'email', 
            'profile_picture', 'followers_count', 'following_count',
        ]
    

class UserDetailSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)  
    following_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'profile_picture',
            'bio', 'followers_count', 'following_count'
        ]
        read_only_fields = ['id', 'email', 'followers_count', 'following_count']

