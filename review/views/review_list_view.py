from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from django.db.models import Q
import json
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication


class RestaurantReviewListView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewInfoSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Review.objects.filter(restaurant_id = restaurant_id)
    
    def list(self, request, *args, **kwargs):
        restaurant = self.get_serializer(self.get_queryset(), many = True)
        res = {
            "msg" : "해당 식당의 모든 리뷰 불러오기 성공",
            "data" : restaurant.data
        }
        return Response(res)