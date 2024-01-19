from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from django.db.models import Q
    

class SearchRestaurantView(APIView):
    def get(self, request, query):
        restaurant = Restaurant.objects.filter(name__contains = query)
        serializer = RestaurantSearchSerializer(restaurant, context={'request': request}, many = True)
        res = {
            "msg" : "식당 이름으로 검색 성공",
            "data" : serializer.data
        }
        return Response(res, status = status.HTTP_200_OK)