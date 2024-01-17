from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from django.shortcuts import get_object_or_404

class RestaurantDetailView(APIView):
    """
    식당 세부 정보 view
    """
    def get(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
        serializer = RestaurantDetailSerializer(restaurant, context={'request': request})
        # res = {
        #     "msg" : "식당 세부 정보 반환 성공",
        #     "data" : serializer.data
        # }
        res = serializer.data
        return Response(res, status = status.HTTP_200_OK)
    

class RestaurantListView(ListAPIView):
    """
    모든 식당 리스트 확인(개발자용)
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantInfoSerializer
