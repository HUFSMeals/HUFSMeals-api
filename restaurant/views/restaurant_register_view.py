from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..serializers import *
from ..models import *
from django.db.models import Q
import json
from django.shortcuts import get_object_or_404
import requests
from decouple import config

food_lst = ['SchoolFood', 'Alchohol', 'Korean', 'Cafe', 'Chinese', 'FastFood', 'Japanese', 'Meat', 'Western', 'WorldFood']

def get_coordinate(address):
    """
    주소 -> 좌표 변환 메소드
    """
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
        coordinate_lst = []
    else:
        latitude = response['documents'][0]['x']
        longtitude = response['documents'][0]['y']
        coordinate_lst = [latitude, longtitude]

    return coordinate_lst


class RestaurantRegisterView(APIView):
    """
    식당 등록 view
    """
    serializer_class = CreateRestaurantSerializer
    # queryset = Restaurant.objects.all()

    def post(self, request):
        data = request.data

        coordinate_lst = get_coordinate(data['address'])
        if len(coordinate_lst) == 0:
            res = {
                "msg" : "올바르지 않은 주소"
            }
            return Response(res)
        
        if data['category'] not in food_lst:
            res = {
                "msg" : "올바르지 않은 카테고리"
            }
            return Response(res)
        serializer = CreateRestaurantSerializer(data = data)
        if serializer.is_valid():
            new_restaurant = serializer.save(latitude = coordinate_lst[0], longitude = coordinate_lst[1])
            res = {
            "msg" : "식당 등록 성공",
            "data" : RestaurantInfoSerializer(new_restaurant).data
        }
        else:
            res = {
                "msg":"올바르지 않은 양식"
            }
        
        return Response(res)
    
"""
case "SchoolFood":
      return PicSchoolFood;
    case "Alchohol":
      return PicAlchohol;
    case "Korean":
      return PicKorean;
    case "Cafe":
      return PicCafe;
    case "Chinese":
      return PicChinese;
    case "FastFood":
      return PicFastFood;
    case "Japanese":
      return PicJapanese;
    case "Meat":
      return PicMeat;
    case "Western":
      return PicWestern;
    case "WorldFood":
      return PicWorldFood;
"""


class RestaurantUpdateView(UpdateAPIView):
    """
    식당 정보 수정 view
    """
    serializer_class = CreateRestaurantSerializer
    queryset = Restaurant.objects.all()
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
