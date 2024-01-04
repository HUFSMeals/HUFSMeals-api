from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from django.db.models import Q
import json
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication


class ReviewImageView(CreateAPIView):
    """
    이미지 업로드 view
    """
    serializer_class = ReviewImageSerializer

    def create(self, request, review_id):
        review = get_object_or_404(Review, pk = review_id)

        serializer = ImageUploadSerializer(data = request.data)
        if serializer.is_valid():
            instance = serializer.save(review = review)
            image = ReviewImage.objects.get(pk = instance.pk)

            res = {
                "msg" : "이미지 업로드 성공",
                "data" : ImageSetSerializer(image, context={'request': request}).data
            }
            
            return Response(res)
        else:
            return Response(serializer.errors)