from rest_framework import serializers
from .models import PostModel
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
# User = get_user_model()




class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        # extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],

        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class PostModelSerializer(serializers.ModelSerializer):
    # author=UserSerializer()
    class Meta:
        model=PostModel
        fields=("title","body","author")


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
