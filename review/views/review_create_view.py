from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from translator.views.langCode_view import langcode_dev
        

class ReviewCreateView(CreateAPIView):
    """
    리뷰 업로드 view
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = CreateReviewSerializer
    
    def create(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
        user = request.user
        src_lang = langcode_dev(request.data['body'])
        score = request.data['score']

        restaurant.review_cnt += 1
        restaurant.score_accum += int(score)
        restaurant.score_avg = (restaurant.score_accum/restaurant.review_cnt)
        restaurant.save()
        

        data = {
            'title' : request.data['title'],
            'body' : request.data['body'],
            'score': score
        }

        serializer = CreateReviewSerializer(data = data)
        
        if serializer.is_valid():
            isinstance = serializer.save(user = user, restaurant = restaurant, src_lang = src_lang)
            review = Review.objects.get(pk = isinstance.pk)
            res = {
                "msg" : "리뷰 작성 성공",
                "data" : ReviewInfoSerializer(review).data
            }
            return Response(res, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)