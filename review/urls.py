from django.urls import path
from review.views import *

app_name = 'review'

urlpatterns = [
    path('create/<int:restaurant_id>/', ReviewCreateView.as_view()),
    path('update/<int:review_id>/', ReviewUpdateView.as_view()),
    path('delete/<int:review_id>/', ReviewDeleteView.as_view()),
    path('image/upload/<int:review_id>/', ReviewImageView.as_view()),
    path('image/original/<int:pk>/', OriginalImageView.as_view()),
    path('image/', AllImageView.as_view()),
    path('restaurant/<int:restaurant_id>/', RestaurantReviewListView.as_view()),
    path('user/<int:user_id>/', UserReviewListView.as_view()),
    path('myreview/', MyReviewListView.as_view()),
]