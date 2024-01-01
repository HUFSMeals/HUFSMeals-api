from rest_framework import serializers
from .models import Restaurant, Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    meuns = MenuSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'