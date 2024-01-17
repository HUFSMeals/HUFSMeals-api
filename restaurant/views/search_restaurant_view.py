from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from django.db.models import Q


class SearchRestaurantView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSearchSerializer

    def get_queryset(self):
        restaurant_name = self.kwargs.get('query')
        return Restaurant.objects.filter(name__contains = restaurant_name)
    
    def list(self, request, *args, **kwargs):
        restaurant = self.get_serializer(self.get_queryset(), context={'request': request}, many = True)
        res = {
            "msg" : "식당 이름으로 검색 성공",
            "data" : restaurant.data
        }
        return Response(res, status = status.HTTP_200_OK)
