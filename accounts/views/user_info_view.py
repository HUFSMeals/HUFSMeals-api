from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import *
from ..serializers import *

class SetNickname(APIView):
    """
    유저 닉네임 설정 view
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
    

class UserInfoView(APIView):
    """
    유저 정보 view
    """
    def get(self, request, user_id):
        user = User.objects.get(pk = user_id)
        serializer = UserInfoSerializer(user)
        res = {
            "msg" : "유저 정보 반환 성공",
            "data" : serializer.data
        }
        return Response(res, status=status.HTTP_200_OK)