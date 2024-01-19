import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from review.models import *
from django.db.models import Q
from decouple import config


def translate_func(pk, target):
    review = Review.objects.get(pk = pk)
    exsiting_review =  review.translated_review.filter(src_lang = target)
    if exsiting_review.exists():
        return exsiting_review.first().body
    translate_api = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {
        'X-Naver-Client-Id' : config('client_id'),
        'X-Naver-Client-Secret' : config('secret')
    }
    data = {
        "source" : review.src_lang,
        "target" : target,
        "text" : review.body
    }
    response = requests.post(translate_api, headers=headers, data=data).json()

    if 'errorCode' in response:
        return review.body
    text = response['message']['result']['translatedText']
    TranslatedReview(review = review, body = text, src_lang = target).save()
    return text


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
        
        # 번역본이 이미 DB에 있을 경우
        exsiting_review =  review.translated_review.filter(src_lang = target)
        if exsiting_review.exists():
            data = {
                "text" : exsiting_review.first().body,
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
            'X-Naver-Client-Id' : config('client_id'),
            'X-Naver-Client-Secret' : config('secret')
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
        TranslatedReview(review = review, body = query_data['text'], src_lang = target).save()

        return Response(res, status=status.HTTP_200_OK)