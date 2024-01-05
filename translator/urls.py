from django.urls import path
from translator.views import *

app_name = 'translator'

urlpatterns = [
    # 언어 코드 확인
    path('langcode/', GetLangCode.as_view()),
    path('<int:review_id>/', Translate.as_view()),
]