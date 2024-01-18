from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
import requests

def translate_func(pk, target):
    review = Review.objects.get(pk = pk)
    exsiting_review =  review.translated_review.filter(src_lang = target)
    if exsiting_review.exists():
        return exsiting_review.first().body
    translate_api = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {
        'X-Naver-Client-Id' : "cGwhwDRITcSEobTG98HL",
        'X-Naver-Client-Secret' : "mNrbhhkyEC"
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


class RestaurantDetailView(APIView):
    """
    식당 세부 정보 view
    """
    def get(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
        data = RestaurantDetailSerializer(restaurant, context={'request': request}).data
        # data['score_avg'] = float(data['score_avg'])
        # res = {
        #     "msg" : "식당 세부 정보 반환 성공",
        #     "data" : serializer.data
        # }
        res = data
        return Response(res, status = status.HTTP_200_OK)
    

class RestaurantListView(ListAPIView):
    """
    모든 식당 리스트 확인(개발자용)
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantInfoSerializer


class RestaurantDetailView2(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request, restaurant_id):
        language = request.user.language
        restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
        serializer = RestaurantPageSerializer(restaurant, context={'request': request})
    
        data = serializer.data
        for i in data['review']:
            if i['src_lang'] != language:
                i['body'] = translate_func(i['id'], language)

        res = {
            "msg" : "식당 세부정보 불러오기 성공",
            "data" : data
        }
        return Response(res, status = status.HTTP_200_OK)