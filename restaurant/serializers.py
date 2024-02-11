from rest_framework import serializers
from .models import *
from review.serializers import *

class CreateRestaurantSerializer(serializers.ModelSerializer):
    """
    식당 생성 시리얼라이저
    """
    class Meta:
        model = Restaurant
        exclude = ['review_cnt', 'score_avg', 'score_accum', 'latitude', 'longitude']

    def get_retaurant_image(self, obj):
        if obj.restaurant_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.restaurant_image.url)
        return None


class RestaurantInfoSerializer(serializers.ModelSerializer):
    """
    식당 상세정보 시리얼라이저
    """
    class Meta:
        model = Restaurant
        fields = '__all__'

    def get_retaurant_image(self, obj):
        if obj.restaurant_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.restaurant_image.url)
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['score_avg'] = float(representation['score_avg'])
        return representation


class RestaurantDetailSerializer(serializers.ModelSerializer):
    """
    식당 디테일 페이지 시리얼라이저
    """
    class Meta:
        model = Restaurant
        exclude = ['latitude', 'longitude', 'score_accum']

    def get_retaurant_image(self, obj):
        if obj.restaurant_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.restaurant_image.url)
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['score_avg'] = float(representation['score_avg'])
        return representation


class AddressSerializer(serializers.ModelSerializer):
    """
    좌표를 얻기 위한 주소 시리얼라이저
    """
    class Meta:
        model = Restaurant
        fields = ['address']



class CreateMenuSerializer(serializers.ModelSerializer):
    """
    메뉴 생성 시리얼라이저
    """
    class Meta:
        model = Menu
        fields = ['name', 'menu_image']


class MenuInfoSerializer(serializers.ModelSerializer):
    """
    메뉴 정보 시리얼라이저
    """
    class Meta:
        model = Menu
        fields = '__all__'

    def get_menu_image(self, obj):
        if obj.menu_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.menu_image.url)
        return None


class RestaurantSearchSerializer(serializers.ModelSerializer):
    """
    식당 검색 결과 시리얼라이저
    """
    class Meta:
        model = Restaurant
        fields = ['id', 'restaurant_image', 'name', 'score_avg', 'review_cnt', 'address', 'category']

    def get_retaurant_image(self, obj):
        if obj.restaurant_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.restaurant_image.url)
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['score_avg'] = float(representation['score_avg'])
        return representation

    
class RestaurantLocationSerializer(serializers.ModelSerializer):
    """
    식당 위/경도 시리얼라이저
    """
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'latitude', 'longitude', 'category', 'address', 'phone', 'review_cnt', 'score_avg']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['score_avg'] = float(representation['score_avg'])
        representation['latitude'] = float(representation['latitude'])
        representation['longitude'] = float(representation['longitude'])
        return representation


class RestaurantPageSerializer(serializers.ModelSerializer):
    review = ReviewInfoSerializer(many = True)
    menu = MenuInfoSerializer(many = True)
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'restaurant_image', 'opening_hours', 'address', 'category', 'phone', 'review_cnt', 'score_avg', 'review', 'menu']
    
    def get_retaurant_image(self, obj):
        if obj.restaurant_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.restaurant_image.url)
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['score_avg'] = float(representation['score_avg'])
        return representation