# accounts/urls.py
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # 토큰
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # kakao
    path('kakao/login/', KakaoLoginView.as_view()),
    path('kakao/callback/', KakaoCallbackView.as_view()),
    path('logout/', LogoutView.as_view()),
    #마이페이지
    path('user/mypage/', MyPage.as_view(), name='mypage'),
    path('user/mypage/report/', MyReports.as_view(), name='my_reports'),
    path('user/mypage/report/<int:reportId>/', ReportDetail.as_view(), name='report_detail'),
    path('user/mypage/type/', ChangeUserType.as_view(), name='change_user_type'),
    path('user/mypage/alarm/', ChangeAlarmOption.as_view(), name='change_alarm_option'),
    path('user/mypage/time/', ChangeAlarmTime.as_view(), name='change_alarm_time'),
    path('user/mypage/distance/', ChangeAlarmDistance.as_view(), name='change_alarm_distance'),

]