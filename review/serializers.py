from rest_framework import serializers
from .models import *
from accounts.serializers import *

# class OriginalImageSerializer(serializers.ModelSerializer):
#     original_image = serializers.SerializerMethodField()
#     """
#     리뷰 사진 원본 시리얼라이저
#     """
    
#     class Meta:
#         model = ReviewImage
#         fields = ['original_image']

#     def get_original_image(self, obj):
#         if obj.original_image:
#             request = self.context.get('request')
#             return request.build_absolute_uri(obj.original_image.url)
#         return None
    

# class ImageUploadSerializer(serializers.ModelSerializer):
#     """
#     리뷰 사진 업로드 시리얼라이저
#     """
    
#     class Meta:
#         model = ReviewImage
#         fields = ['original_image']


# class ThumbImageSerializer(serializers.ModelSerializer):
#     """
#     축소된 이미지 시리얼라이저
#     """
#     review_image = serializers.SerializerMethodField()

#     class Meta:
#         model = ReviewImage
#         fields = ['id', 'review_image']

#     def get_review_image(self, obj):
#         if obj.review_image:
#             request = self.context.get('request')
#             return request.build_absolute_uri(obj.review_image.url)
#         return None


# class ImageSetSerializer(serializers.ModelSerializer):
#     review_image = serializers.SerializerMethodField()
#     original_image = serializers.SerializerMethodField()

#     class Meta:
#         model = ReviewImage
#         fields = ['id', 'review_image', 'original_image']

#     def get_original_image(self, obj):
#         if obj.original_image:
#             request = self.context.get('request')
#             return request.build_absolute_uri(obj.original_image.url)
#         return None
    
#     def get_review_image(self, obj):
#         if obj.review_image:
#             request = self.context.get('request')
#             return request.build_absolute_uri(obj.review_image.url)
#         return None


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def get_review_image(self, obj):
        if obj.review_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.review_image.url)
        return None


class CreateReviewSerializer(serializers.ModelSerializer):
    """
    리뷰 생성 시리얼라이저
    """
    class Meta:
        model = Review
        fields = ['title', 'body', 'score']


class ReviewInfoSerializer(serializers.ModelSerializer):
    """
    리뷰 정보 시리얼라이저
    """
    image = ReviewImageSerializer(many = True)
    user = UserInfoSerializer()
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