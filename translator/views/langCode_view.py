import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

client_id = "cGwhwDRITcSEobTG98HL"
secret = "mNrbhhkyEC"

def langcode_dev(text):
    """
    개발용 언어 감지 메소드
    """
    code_api = "https://openapi.naver.com/v1/papago/detectLangs"
    headers = {
        'X-Naver-Client-Id' : client_id,
        'X-Naver-Client-Secret' : secret
    }
    data = {
        "query" : text
    }
    response = requests.post(code_api, headers=headers, data = data).json()
    src_lang = response['langCode']
    return src_lang


class GetLangCode(APIView):
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
                "code" : "t-F002",
                "msg" : "API 사용량 초과"
            }
            return Response(res, status = status.HTTP_403_FORBIDDEN)