from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from django.shortcuts import get_object_or_404

class RestaurantLocationView(APIView):
    def get(self, request):
        restaurant = Restaurant.objects.all()
        serializer = RestaurantLocationSerializer(restaurant, many = True)
        res = {
            "msg" : "식당 위/경도 반환 성공",
            "data" : serializer.data
        }
        return Response(res, status = status.HTTP_200_OK)