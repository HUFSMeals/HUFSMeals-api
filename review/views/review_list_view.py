from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from rest_framework_simplejwt.authentication import JWTAuthentication


class RestaurantReviewListView(ListAPIView):
    """
    특정 식당의 리뷰 불러오기 view
    """
    queryset = Review.objects.all()
    serializer_class = ReviewInfoSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Review.objects.filter(restaurant_id = restaurant_id)
    
    def list(self, request, *args, **kwargs):
        review = self.get_serializer(self.get_queryset(), many = True)
        res = {
            "msg" : "해당 식당의 모든 리뷰 불러오기 성공",
            "data" : review.data
        }
        return Response(res, status = status.HTTP_200_OK)
    

class UserReviewListView(ListAPIView):
    """
    특정 유저의 리뷰 불러오기 view
    """
    queryset = Review.objects.all()
    serializer_class = ReviewInfoSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Review.objects.filter(user_id = user_id)
    
    def list(self, request, *args, **kwargs):
        review = self.get_serializer(self.get_queryset(), many = True)
        res = {
            "msg" : "해당 유저의 모든 리뷰 불러오기 성공",
            "data" : review.data
        }
        return Response(res, status = status.HTTP_200_OK)
    

class MyReviewListView(ListAPIView):
    """
    나의 리뷰 불러오기 view
    """
    queryset = Review.objects.all()
    serializer_class = ReviewInfoSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Review.objects.filter(user = self.request.user)
    
    def list(self, request, *args, **kwargs):
        review = self.get_serializer(self.get_queryset(), many = True)
        res = {
            "msg" : "나의 모든 리뷰 불러오기 성공",
            "data" : review.data
        }
        return Response(res, status = status.HTTP_200_OK)