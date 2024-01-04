from django.urls import path
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('login/<str:code>/', GoogleLogin.as_view()),
    path('nickname/', SetNickname.as_view()),
    path('info/<int:user_id>/', UserInfoView.as_view()),

    # 개발자용
    path('google/', GoogleLoginApi.as_view()),
    path('login/', DevGoogleLogin.as_view()),
]