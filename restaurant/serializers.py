from rest_framework import serializers
from .models import *

class CreateRestaurantSerializer(serializers.ModelSerializer):
    """
    식당 생성 시리얼라이저
    """
    class Meta:
        model = Restaurant
        exclude = ['review_cnt', 'score_avg']


class RestaurantInfoSerializer(serializers.ModelSerializer):
    """
    식당 정보 시리얼라이저
    """
    class Meta:
        model = Restaurant
        fields = '__all__'


class CreateMenuSerializer(serializers.ModelSerializer):
    """
    메뉴 생성 시리얼라이저
    """
    class Meta:
        model = Menu
        fields = ['name', 'image']


class MenuInfoSerializer(serializers.ModelSerializer):
    """
    메뉴 정보 시리얼라이저
    """
    class Meta:
        model = Menu
        fields = '__all__'