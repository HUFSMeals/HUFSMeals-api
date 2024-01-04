from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from django.db.models import Q
import json
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
        

class ReviewCreateView(CreateAPIView):
    """
    리뷰 업로드 view
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = CreateReviewSerializer
    
    def create(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
        user = request.user
        src_lang = "test"
        score = 5

        data = {
            'user': user,
            'title' : request.data['title'],
            'body' : request.data['body'],
            'restaurant': restaurant,
            'src_lang': src_lang,
            'score': score
        }

        serializer = CreateReviewSerializer(data = data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)