from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from django.shortcuts import get_object_or_404


class NoticeListView(APIView):
    def get(self, request):
        queryset = Notice.objects.all()
        serializer = NoticeListSerializer(queryset, many = True)
        
        res = {
            "msg" : "공지사항 목록 불러오기 성공",
            "data" : serializer.data
        }
        return Response(res, status = status.HTTP_200_OK)
    

class NoticeDetailView(APIView):
    def get(self, request, notice_id):
        query = get_object_or_404(Notice, id = notice_id)
        serializer = NoticeDetailSerializer(query)

        res = {
            "msg" : "공지사항 세부정보 불러오기 성공",
            "data" : serializer.data
        }
        return Response(res, status = status.HTTP_200_OK)