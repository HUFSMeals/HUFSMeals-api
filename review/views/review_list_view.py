from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from restaurant.serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
import requests
from decouple import config

def translate_func(pk, target):
    review = Review.objects.get(pk = pk)
    exsiting_review =  review.translated_review.filter(src_lang = target)
    if exsiting_review.exists():
        return exsiting_review.first().body
    translate_api = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {
        'X-Naver-Client-Id' : config('client_id'),
        'X-Naver-Client-Secret' : config('secret')
    }
    data = {
        "source" : review.src_lang,
        "target" : target,
        "text" : review.body
    }
    response = requests.post(translate_api, headers=headers, data=data).json()

    if 'errorCode' in response:
        return review.body
    text = response['message']['result']['translatedText']
    TranslatedReview(review = review, body = text, src_lang = target).save()
    return text


class RestaurantReviewListView(ListAPIView):
    """
    특정 식당의 리뷰 불러오기 view
    """
    queryset = Review.objects.all()
    serializer_class = ReviewInfoSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Review.objects.filter(restaurant_id = restaurant_id)
    
    def list(self, request, *args, **kwargs):
        data = self.get_serializer(self.get_queryset(), many = True).data
        language = request.user.language
        for i in data:
            if i['src_lang'] != language:
                i['body'] = translate_func(i['id'], language)
        res = {
            "msg" : "해당 식당의 모든 리뷰 불러오기 성공",
            "data" : data
        }
        return Response(res, status = status.HTTP_200_OK)
    

class UserReviewListView(ListAPIView):
    """
    특정 유저의 리뷰 불러오기 view
    """
    queryset = Review.objects.all()
    serializer_class = ReviewInfoSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Review.objects.filter(user_id = user_id)
    
    def list(self, request, *args, **kwargs):
        data = self.get_serializer(self.get_queryset(), many = True).data
        language = request.user.language
        for i in data:
            if i['src_lang'] != language:
                i['body'] = translate_func(i['id'], language)
        res = {
            "msg" : "해당 유저의 모든 리뷰 불러오기 성공",
            "data" : data
        }
        return Response(res, status = status.HTTP_200_OK)
    

class MyReviewListView(ListAPIView):
    """
    나의 리뷰 불러오기 view
    """
    queryset = Review.objects.all()
    serializer_class = ReviewInfoSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Review.objects.filter(user = self.request.user)
    
    def list(self, request, *args, **kwargs):
        review = self.get_serializer(self.get_queryset(), many = True)
        res = {
            "msg" : "나의 모든 리뷰 불러오기 성공",
            "data" : review.data
        }
        return Response(res, status = status.HTTP_200_OK)
    

class ReviewRestaurantInfoView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, review_id):
        review = Review.objects.get(pk = review_id)
        restaurant_info = RestaurantSimpleSerializer(review.restaurant, context={'request': request})
        res = {
            "msg" : "리뷰 식당 정보 반환 성공",
            "data" : restaurant_info.data
        }
        return Response(res, status=status.HTTP_200_OK)