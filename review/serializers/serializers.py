from rest_framework import serializers
from ..models import *
from accounts.serializers import *
from rest_framework.fields import SerializerMethodField


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = '__all__'

    def get_review_image(self, obj):
        if obj.review_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.review_image.url)
        return None
    

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['review_image']


class CreateReviewSerializer(serializers.ModelSerializer):
    """
    리뷰 생성 시리얼라이저
    """
    class Meta:
        model = Review
        fields = ['title', 'body', 'score']


class TranslatedReviewSerializer(serializers.ModelSerializer):
    """
    번역된 리뷰 시리얼라이저
    """
    class Meta:
        model = TranslatedReview
        fields = '__all__'


# from restaurant.serializers import RestaurantInfoSerializer

class ReviewInfoSerializer(serializers.ModelSerializer):
    """
    리뷰 정보 시리얼라이저
    """
    review_image = ReviewImageSerializer(many = True)
    user = UserInfoSerializer()
    restaurant = SerializerMethodField()
    class Meta:
        model = Review
        fields = '__all__'

    def get_restaurant(self, obj):
        from restaurant.serializers import RestaurantInfoSerializer
        serializer = RestaurantInfoSerializer(obj.restaurant, context=self.context)
        return serializer.data