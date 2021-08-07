from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import ForumPost, ForumComment, ForumReply, Events, UserExtension


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class ForumPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumPost
        fields = '__all__'


class ForumCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumComment
        fields = '__all__'


class ForumReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumReply
        fields = '__all__'


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'


class UserExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtension
        fields = '__all__'
