from rest_framework import serializers
from .models import *

class CreateRestaurantSerializer(serializers.ModelSerializer):
    """
    식당 생성 시리얼라이저
    """
    class Meta:
        model = Restaurant
        exclude = ['review_cnt', 'score_avg', 'score_accum']


class RestaurantInfoSerializer(serializers.ModelSerializer):
    """
    식당 정보 시리얼라이저
    """
    class Meta:
        model = Restaurant
        fields = '__all__'


class RestaurantDetailSerializer(serializers.ModelSerializer):
    """
    식당 디테일 페이지 시리얼라이저
    """
    class Meta:
        model = Restaurant
        exclude = ['latitude', 'longitude', 'score_accum']


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


class RestaurantSearchSerializer(serializers.ModelSerializer):
    """
    식당 검색 결과 시리얼라이저
    """
    class Meta:
        model = Restaurant
        fields = ['id', 'restaurant_image', 'name', 'score_avg', 'review_cnt', 'address', 'category']

    
class RestaurantLocationSerializer(serializers.ModelSerializer):
    """
    식당 위/경도 시리얼라이저
    """
    class Meta:
        model = Restaurant
        fields = ['id', 'latitude', 'longitude', 'category']