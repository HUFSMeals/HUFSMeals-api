from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from ..models import Restaurant, Menu
from ..serializers import RestaurantSerializer, MenuSerializer
# Create your views here.

class RestaurantViewSet(RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuViewSet(RetrieveAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer