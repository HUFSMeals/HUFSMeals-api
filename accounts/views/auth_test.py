from rest_framework.views import APIView, View
import requests
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from ..models import *
from ..serializers import *

lang_lst = ['ko', 'en', 'ja', 'zh-CN', 'zh-TW', 'vi', 'id', 'th', 'de', 'ru', 'es', 'it', 'fr']


class GetCodeView(APIView):
    def get(self, request):
        code = request.GET["code"]
        address = "http://127.0.0.1:8000/"

        return redirect(f"{address}accounts/login/?code={code}")