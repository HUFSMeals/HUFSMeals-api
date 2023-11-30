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

class GetLangCode(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        text = request.data['text']
        code_api = "https://openapi.naver.com/v1/papago/detectLangs"
        headers = {
            'X-Naver-Client-Id' : client_id,
            'X-Naver-Client-Secret' : secret
        }
        data = {
            "query" : text
        }
        response = requests.post(code_api, headers=headers, data = data).json()

        # if response
        if 'langCode' in response:
            if response['langCode'] == "unk":
                res = {
                    "code" : "t-F001",
                    "msg" : "언어 감지 실패",
                    "data" : response
                }
                return Response(res, status = status.HTTP_400_BAD_REQUEST)
            else:
                res = {
                    "code" : "t-S001",
                    "msg" : "언어 감지 성공",
                    "data" : response
                }
                return Response(res, status = status.HTTP_200_OK)
        else:
            res = {
                "code" : "t-F001",
                "msg" : "API 사용량 초과"
            }
            return Response(res, status = status.HTTP_403_FORBIDDEN)