from django.urls import path
from restaurant.views import *

app_name = 'restaurant'

urlpatterns = [
    path('', RestaurantListView.as_view()),
    path('create/', RestaurantRegisterView.as_view()),
    path('detail/<int:restaurant_id>/', RestaurantDetailView.as_view()),
    path('search/<str:query>/', SearchRestaurantView.as_view()),
    path('location/', RestaurantLocationView.as_view()),
    path('menu/<int:restaurant_id>/', MenuListView.as_view()),
]