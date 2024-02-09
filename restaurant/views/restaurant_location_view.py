from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from django.shortcuts import get_object_or_404
from decouple import config
import requests

class RestaurantLocationView(APIView):
    def get(self, request):
        restaurant = Restaurant.objects.all()
        serializer = RestaurantLocationSerializer(restaurant, many = True)
        res = {
            "msg" : "식당 위/경도 반환 성공",
            "data" : serializer.data
        }
        return Response(res, status = status.HTTP_200_OK)
    

class GetCoordinateView(APIView):
    serializer_class = AddressSerializer
    def get(self, request, address):
        # address = request.data.get('address')
        api_address = "https://dapi.kakao.com/v2/local/search/address.json"

        headers = {
            "Authorization" : f"KakaoAK {config('kakao_app_key')}"
        }
        data = {
            "query" : address,
            "analyze_type" : "exact",
        }

        response = requests.get(api_address, headers=headers, data=data).json()

        if len(response['documents']) == 0:
            res = {
                "msg" : '잘못된 주소'
            }
        else:
            latitude = response['documents'][0]['x']
            longtitude = response['documents'][0]['y']
            res = {
                '위도' : latitude,
                '경도' : longtitude
            }

        return Response(res)