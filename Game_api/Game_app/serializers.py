from django.db import models
from Game_app.models import Developer
from Game_app.models import GameMaker
from Game_app.models import device_frant
from rest_framework.serializers import ModelSerializer
from Game_app.models import User
from rest_framework import serializers


class DeveloperSerializer(ModelSerializer):
    class Meta:
        model = Developer
        fields = '__all__'


class GameMakerSerializer(ModelSerializer):
    # developer = DeveloperSerializer()

    class Meta:
        model = GameMaker
        fields = '__all__'


class device_frantSerializer(ModelSerializer):
    # developer = DeveloperSerializer()

    class Meta:
        model = device_frant
        fields = '__all__'

class UserSerializer(ModelSerializer):

    class Meta:
        model=User
        field=['email','password','is_verified']


class verifyAccountSerilizer(ModelSerializer):
    email=serializers.EmailField()
    otp=serializers.CharField()
