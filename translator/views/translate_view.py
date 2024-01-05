from django.shortcuts import render
from rest_framework.decorators import api_view
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
import json

client_id = "cGwhwDRITcSEobTG98HL"
secret = "mNrbhhkyEC"

class Translate(APIView):
    """
    파파고 번역 api view
    """
    def post(self, request):
        text = request.data['text']
        source = request.data['source']

        if self.request.user.country == source:
            res = {
                "msg" : "번역 source/target 언어가 동일",
                "code" : "t-F005"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        translate_api = "https://openapi.naver.com/v1/papago/n2mt"
        headers = {
            'X-Naver-Client-Id' : client_id,
            'X-Naver-Client-Secret' : secret
        }
        data = {
            "source" : source,
            "target" : self.request.user.country,
            "text" : text
        }

        response = requests.post(translate_api, headers=headers, data=data).json()

        if 'errorCode' in response:
            if response['errorCode'] == "N2T08":
                res = {
                    "msg" : "텍스트 용량 초과",
                    "code" : "t-F003"
                }
            else:
                res = {
                    "msg" : "api 사용량 초과",
                    "code" : "t-F004"
                }
            return Response(res, status = status.HTTP_400_BAD_REQUEST)
        
        query_data = {
            "text" : response['message']['result']['translatedText'],
            "source" : response['message']['result']['srcLangType'],
            "target" : response['message']['result']['tarLangType']
        }

        res = {
            "msg" : "번역 성공",
            "code" : "t-S001",
            "data" : query_data
        }

        return Response(response, status=status.HTTP_200_OK)