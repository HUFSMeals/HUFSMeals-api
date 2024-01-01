from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import *
from ..serializers import *

class SetNickname(APIView):
    """
    유저 닉네임 설정
    """
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = self.request.user
        nickname = request.data['nickname']
        user.nickname = nickname
        user.save()

        res = {
            "msg" : "닉네임 설정 성공",
            "code" : "a-S003"
        }

        return Response(res, status = status.HTTP_200_OK)