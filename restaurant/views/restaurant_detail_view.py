from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from django.shortcuts import get_object_or_404

class RestaurantDetailView(APIView):
    def get(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
        serializer = RestaurantDetailSerializer(restaurant)
        res = {
            "msg" : "식당 세부 정보 반환 성공",
            "data" : serializer.data
        }
        return Response(res, status = status.HTTP_200_OK)