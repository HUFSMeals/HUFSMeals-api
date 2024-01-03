from rest_framework import serializers
from .models import *

class ReviewImageSerializer(serializers.ModelSerializer):
    """
    리뷰 사진 시리얼라이저
    """
    class Meta:
        model = ReviewImage
        fields = '__all__'


class CreateReviewSerializer(serializers.ModelSerializer):
    """
    리뷰 생성 시리얼라이저
    """
    class Meta:
        model = Review
        exclude = ['user', 'restaurant', 'src_lang']


class ReviewInfoSerializer(serializers.ModelSerializer):
    """
    리뷰 정보 시리얼라이저
    """
    image = ReviewImageSerializer(many = True)
    class Meta:
        model = Review
        fields = '__all__'


class TranslatedReviewSerializer(serializers.ModelSerializer):
    """
    번역된 리뷰 시리얼라이저
    """
    class Meta:
        model = TranslatedReview
        fields = '__all__'