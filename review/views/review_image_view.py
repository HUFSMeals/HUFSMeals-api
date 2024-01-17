from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from django.shortcuts import get_object_or_404


class ReviewImageView(CreateAPIView):
    """
    이미지 업로드 view
    """
    serializer_class = ReviewImageSerializer

    def create(self, request, review_id):
        review = get_object_or_404(Review, pk = review_id)

        serializer = ReviewImageSerializer(data = request.data)
        if serializer.is_valid():
            instance = serializer.save(review = review)
            image = ReviewImage.objects.get(pk = instance.pk)

            res = {
                "msg" : "이미지 업로드 성공",
                "data" : ReviewImageSerializer(image, context={'request': request}).data
            }
            
            return Response(res, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
        

class OriginalImageView(RetrieveAPIView):
    """
    이미지 원본 불러오기 view
    """
    queryset = ReviewImage.objects.all()
    serializer_class = ReviewImageSerializer
    lookup_field = 'pk'
    

class AllImageView(ListAPIView):
    """
    (개발용)DB상 모든 이미지 데이터 확인 view
    """
    serializer_class = ReviewImageSerializer
    queryset = ReviewImage.objects.all()