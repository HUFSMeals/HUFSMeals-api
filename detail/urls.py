from django.urls import path
from .views.detail_views import *

app_name = 'detail'

urlpatterns = [
    path('restaurants/<int:pk>/', RestaurantViewSet.as_view())
]