from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from django.shortcuts import get_object_or_404


class MenuListView(APIView):
    """
    식당 메뉴 view
    """
    def get(self, request, restaurant_id):
        menus = Menu.objects.filter(restaurant = restaurant_id)
        serializer = MenuInfoSerializer(menus, many = True)
        return Response(serializer.data)
    

class CreateMenuView(CreateAPIView):
    """
    메뉴 등록 view
    """
    def post(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
        serializer = CreateMenuSerializer(data = request.data)
        if serializer.is_valid():
            menu = serializer.save(restaurant = restaurant)
            res = {
                "msg" : "메뉴 등록 완료",
                "data" : MenuInfoSerializer(menu).data
            }
            return Response(res, status = status.HTTP_200_OK)
        else:
            res = {
                "msg" : "유효하지 않은 데이터",
            }
            return Response(res, status = status.HTTP_400_BAD_REQUEST)
        