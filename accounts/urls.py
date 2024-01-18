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

    # 클라이언트 로그인 테스트
    path('signin/', GoogleRedirectView.as_view()),
    path('code/', GetCodeView.as_view()),
    path('userinfo/', GrantTokenView.as_view()),
]

"""
클라이언트 -> 서버(accounts/google/): 구글로 보내는 redirect 객체

클라이언트(redirect) -> 구글: 구글은 쿼리에 인가코드를 담아
accounts/test/로 보내는 redirect 객체를 반환한다

그럼 이 accounts/test/로 리다이렉트하면 json으로 인가코드를 반환한다.


"""