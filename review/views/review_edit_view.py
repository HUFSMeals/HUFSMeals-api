from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..serializers import *
from ..models import *
from django.db.models import Q
import json
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication


class ReviewUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    def put(self, request, review_id):
        review = Review.objects.get(pk = review_id)
        if review.user != request.user:
            res = {
                "msg" : "리뷰 작성자와 유저 불일치"
            }
            return Response(res, status = status.HTTP_400_BAD_REQUEST)
        serializer = UpdateReviewSerializer(review, data = request.data)
        if serializer.is_valid():
            serializer.save()
            res = {
                "msg" : "리뷰 수정 성공"
            }
            return Response(res, status = status.HTTP_200_OK)
        else:
            res = {
                "msg" : "유효하지 않은 입력"
            }
            return Response(res, status = status.HTTP_400_BAD_REQUEST)
        

class ReviewDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    def delete(self, request, review_id):
        review = Review.objects.get(pk = review_id)
        if review.user != request.user:
            res = {
                "msg" : "리뷰 작성자와 유저 불일치"
            }
            return Response(res, status = status.HTTP_400_BAD_REQUEST)
        review.delete()
        res = {
            "msg" : "리뷰 삭제 성공"
        }
        return Response(res, status = status.HTTP_204_NO_CONTENT)