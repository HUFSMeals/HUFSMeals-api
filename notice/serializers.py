from rest_framework import serializers
from .models import *

class NoticeListSerializer(serializers.ModelSerializer):
    """
    공지사항 목록 시리얼라이저
    """
    class Meta:
        model = Notice
        fields = ['title', 'created_at']


class NoticeDetailSerializer(serializers.ModelSerializer):
    """
    공지사항 디테일 시리얼라이저
    """
    class Meta:
        model = Notice
        fields = '__all__'