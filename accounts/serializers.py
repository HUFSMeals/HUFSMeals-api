from rest_framework import serializers
from .models import *

class UserDetailSerializer(serializers.ModelSerializer):
    """
    유저 모든 정보
    """
    class Meta:
        model = User
        fields = '__all__'


class UserInfoSerializer(serializers.ModelSerializer):
    """
    간단한 유저 정보
    """
    class Meta:
        model = User
        fields = ['id', 'nickname', 'country']