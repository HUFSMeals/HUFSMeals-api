from django.urls import path
from notice.views import *

app_name = 'notice'

urlpatterns = [
    path('', NoticeListView.as_view()),
]