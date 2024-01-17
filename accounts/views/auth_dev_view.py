from rest_framework.views import APIView
import requests
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from ..models import *
from ..serializers import *

lang_lst = ['ko', 'en', 'ja', 'zh-CN', 'zh-TW', 'vi', 'id', 'th', 'de', 'ru', 'es', 'it', 'fr']

class GoogleLoginApi(APIView):
    """
    개발자용 구글 로그인 페이지 접속 view
    """
    def get(self, request):
        app_key = "694730838559-u7slukjsulo3h4r0qhjln4ah8lnjmftt.apps.googleusercontent.com"
        scope = "https://www.googleapis.com/auth/userinfo.email " + \
                "https://www.googleapis.com/auth/userinfo.profile"
        
        redirect_uri = "https://hufsmeals/accounts/login/"
        google_auth_api = "https://accounts.google.com/o/oauth2/v2/auth"

        response = redirect(
            f"{google_auth_api}?client_id={app_key}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
        )
        
        return response


class DevGoogleLogin(APIView):
    """
    개발자용 액세슨 토큰 발급 view
    """
    def get(self, request):
        code = request.GET["code"]
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id" : "694730838559-u7slukjsulo3h4r0qhjln4ah8lnjmftt.apps.googleusercontent.com",
            "client_secret" : "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",
            "code" : code,
            "grant_type" : 'authorization_code',
            "redirect_uri" : "https://hufsmeals/accounts/login/"
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