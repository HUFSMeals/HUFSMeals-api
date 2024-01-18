from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from django.db.models import Q
import json
from django.shortcuts import get_object_or_404

class RestaurantRegisterView(CreateAPIView):
    """
    식당 등록 view
    """
    serializer_class = CreateRestaurantSerializer
    queryset = Restaurant.objects.all()


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