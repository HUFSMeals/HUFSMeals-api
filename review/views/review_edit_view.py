from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..serializers import *
from ..models import *
from django.db.models import Q
import json
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from translator.views.langCode_view import langcode_dev


class ReviewUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    def put(self, request, review_id):
        review = Review.objects.get(pk = review_id)
        if review.user != request.user:
            res = {
                "msg" : "리뷰 작성자와 유저 불일치"
            }
            return Response(res, status = status.HTTP_400_BAD_REQUEST)
        src_lang = langcode_dev(request.data['body'])['langCode']
        data = request.data.copy()
        data['src_lang'] = src_lang
        serializer = UpdateReviewSerializer(review, data = data)
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
    

class ImageUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    def get_image(self):
        image = ReviewImage.objects.get(pk = self.kwargs.get('image_id'))
        return image

    def delete(self, request, image_id):
        image = self.get_image()
        if image.review.user != request.user:
            res = {
                "msg" : "리뷰 작성자와 유저 불일치"
            }
            return Response(res, status = status.HTTP_400_BAD_REQUEST)
        image.delete()
        res = {
            "msg" : "리뷰 사진 삭제 성공"
        }
        return Response(res, status = status.HTTP_204_NO_CONTENT)
    
    def put(self, request, image_id):
        image = self.get_image()
        if image.review.user != request.user:
            res = {
                "msg" : "리뷰 작성자와 유저 불일치"
            }
            return Response(res, status = status.HTTP_400_BAD_REQUEST)
        serializer = ImageUploadSerializer(image, request.data)
        if serializer.is_valid():
            serializer.save()
            res = {
                "msg" : "리뷰 사진 수정 성공"
            }
            return Response(res, status = status.HTTP_200_OK)
        else:
            res = {
                "msg" : "유효하지 않은 파일"
            }
            return Response(res, status = status.HTTP_400_BAD_REQUEST)