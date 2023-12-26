from rest_framework import serializers
from .models import category
from .models import Make_and_Models
from .models import make_and_Models_mapping
from Game_app.serializers import GameMakerSerializer


class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = '__all__'


class make_and_ModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make_and_Models
        fields = '__all__'


class make_and_Models_mappingSerializer(serializers.ModelSerializer):
    Game = GameMakerSerializer()

    class Meta:
        model = make_and_Models_mapping
        fields = '__all__'
