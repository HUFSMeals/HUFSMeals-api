from rest_framework.views import APIView, View
import requests
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from ..models import *
from ..serializers import *
from urllib.parse import urlencode
from django.http import JsonResponse

lang_lst = ['ko', 'en', 'ja', 'zh-CN', 'zh-TW', 'vi', 'id', 'th', 'de', 'ru', 'es', 'it', 'fr']


class GoogleLoginView(APIView):
    def get(self, request, *args, **kwargs):
        # 구글 소셜 로그인 URL 생성
        google_login_url = self.get_google_login_url()
        res = {
            "msg" : "구글 로그인 url 리턴 성공",
            "data" : google_login_url
        }
        return Response(res, status = status.HTTP_200_OK)

    def get_google_login_url(self):
        base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
        client_id = '694730838559-u7slukjsulo3h4r0qhjln4ah8lnjmftt.apps.googleusercontent.com'
        redirect_uri = 'https://port-0-hufsmeals-1efqtf2dlrgj6rlh.sel5.cloudtype.app/accounts/test/login/'
        scope = "https://www.googleapis.com/auth/userinfo.email " + \
                "https://www.googleapis.com/auth/userinfo.profile"
        response_type = 'code'

        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'scope': scope,
            'response_type': response_type,
        }

        login_url = f'{base_url}?{urlencode(params)}'
        return login_url

class GoogleCallbackView(APIView):
    def get(self, request, *args, **kwargs):
        # 소셜 로그인 후 콜백에서 처리할 로직 작성
        code = request.GET.get('code')
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id" : "694730838559-u7slukjsulo3h4r0qhjln4ah8lnjmftt.apps.googleusercontent.com",
            "client_secret" : "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",
            "code" : code,
            "grant_type" : 'authorization_code',
            "redirect_uri" : 'https://port-0-hufsmeals-1efqtf2dlrgj6rlh.sel5.cloudtype.app/accounts/test/login/'
        }
        
        access_token = requests.post(token_url, data=data).json().get('access_token')

        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        user_information = requests.get(user_info_url, headers={"Authorization": f"Bearer {access_token}"}).json()

        google_id = str(user_information['id'])

        user = User.objects.filter(google_id = google_id).first()
        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            res = {
                "msg" : "기존 사용자 로그인 성공",
                "code" : "a-S001",
                "data" : {
                    "access_token" : access_token,
                    "user_info" : UserInfoSerializer(user).data, 
                    "exist_user" : True
                }
            }
            return Response(res, status=status.HTTP_200_OK)
        
        language = user_information['locale']
        
        if language not in lang_lst:
            language = "en" # 해당 국가에 대한 번역을 지원하지 않을 경우 영어로 통일

        new_user = User(google_id = google_id, language = language)
        new_user.save()
        token = TokenObtainPairSerializer.get_token(new_user)
        access_token = str(token.access_token)
        res = {
            "msg" : "새로운 사용자 로그인 성공",
            "code" : "a-S002",
            "data" : {
                "access_token" : access_token,
                "exist_user" : False
            }
        }
        return Response(res, status=status.HTTP_200_OK)