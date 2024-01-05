import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from review.models import *
from django.db.models import Q

client_id = "cGwhwDRITcSEobTG98HL"
secret = "mNrbhhkyEC"

class Translate(APIView):
    """
    파파고 번역 api view
    """
    authentication_classes = [JWTAuthentication]

    def get(self, request, review_id):
        review = get_object_or_404(Review, pk = review_id)
        text = review.body
        source = review.src_lang
        target = request.user.language

        if target == source:
            res = {
                "msg" : "번역 source/target 언어가 동일"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        translated_review = TranslatedReview.objects.filter(Q(pk = review_id)&Q(src_lang = target)).first()
        if translated_review:
            data = {
                "text" : translated_review.body,
                "source" : source,
                "target" : target
            }
            res = {
                "msg" : "번역 성공",
                "data" : data
            }
            return Response(res, status = status.HTTP_200_OK)

        translate_api = "https://openapi.naver.com/v1/papago/n2mt"
        headers = {
            'X-Naver-Client-Id' : client_id,
            'X-Naver-Client-Secret' : secret
        }
        data = {
            "source" : source,
            "target" : target,
            "text" : text
        }

        response = requests.post(translate_api, headers=headers, data=data).json()

        if 'errorCode' in response:
            if response['errorCode'] == "N2T08":
                res = {
                    "msg" : "텍스트 용량 초과",
                }
            else:
                res = {
                    "msg" : "api 사용량 초과",
                }
            return Response(res, status = status.HTTP_400_BAD_REQUEST)
        
        query_data = {
            "text" : response['message']['result']['translatedText'],
            "source" : response['message']['result']['srcLangType'],
            "target" : response['message']['result']['tarLangType']
        }

        res = {
            "msg" : "번역 성공",
            "data" : query_data
        }
        new_review = TranslatedReview(review = review, body = query_data['text'], src_lang = target).save()

        return Response(res, status=status.HTTP_200_OK)