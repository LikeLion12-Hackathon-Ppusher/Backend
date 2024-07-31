from django.shortcuts import get_object_or_404, render, redirect
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from report.serializers import ReportSerializer
from .serializers import UserSerializer, RegisterSerializer, AuthSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import logout
from config.settings import *
from .models import User
from report.models import *
import requests

# kakao 관련 uri
kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"


class UserView(APIView):
    permission_classes = [AllowAny]

    # data : request.data
    def create_user(self, data):
        serializer = RegisterSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.create(serializer.validated_data)
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # 계정 조회 및 등록
        return self.get_or_create_user(data=request.data)

class LoginView(APIView):
    permission_classes = [AllowAny]

    # data : request.data
    def object(self, data):
        serializer = AuthSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]
            res = Response(
                {
                    "user": {
                        "userId": user.userId,
                        "userName" : user.name,
                        "userType": user.userType,
                    },
                    "setting" : {
                        "distance" : user.distance,
                        "time" : user.time,
                        "option" : user.option
                    },
                    "message": "login success",
                    "access_token": access_token,
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("refresh-token", refresh_token, httponly=True)
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def post(self, request):
        # 로그인
        return self.object(data=request.data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK)


def login_api(social_id: str, email: str=None, phone: str=None):

    # 회원가입 및 로그인
    login_view = LoginView()
    try:
        User.objects.get(userId=social_id)
        data = {
            'userId': social_id,
            'kakaoEmail': email,
        }
        response = login_view.object(data=data)

    except User.DoesNotExist:
        data = {
            'userId': social_id,
            'kakaoEmail': email,
        }
        user_view = UserView()
        login = user_view.create_user(data=data)

        response = login_view.object(data=data) if login.status_code == 201 else login
        response.status_code = 201

    return response


class KakaoLoginView(APIView):
    permission_classes = [AllowAny,]

    def get(self, request):

        # kakao code 요청
        client_id = KAKAO_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = KAKAO_CONFIG['KAKAO_REDIRECT_URI']
        uri = f"{kakao_login_uri}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        
        res = redirect(uri)
        return res
    
class KakaoCallbackView(APIView):
    permission_classes = [AllowAny]

    # @swagger_auto_schema(query_serializer=CallbackUserInfoSerializer)
    def post(self, request):
        
        # access_token 발급 요청
        data = request.data
        code = data.get('authorizationCode')

        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print(code)
        request_data = {
            'grant_type': 'authorization_code',
            'client_id': KAKAO_CONFIG['KAKAO_REST_API_KEY'],
            'redirect_uri': KAKAO_CONFIG['KAKAO_REDIRECT_URI'],
            'client_secret': KAKAO_CONFIG['KAKAO_CLIENT_SECRET_KEY'],
            'code': code,
        }
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        token_res = requests.post(kakao_token_uri, data=request_data, headers=token_headers)

        token_json = token_res.json()
        access_token = token_json.get('access_token')

        if not access_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        access_token = f"Bearer {access_token}"  # 'Bearer ' 마지막 띄어쓰기 필수

        # kakao 회원정보 요청
        auth_headers = {
            "Authorization": access_token,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        user_info_res = requests.get(kakao_profile_uri, headers=auth_headers)
        user_info_json = user_info_res.json()

        social_type = 'kakao'
        social_id = f"{social_type}_{user_info_json.get('id')}"

        kakao_account = user_info_json.get('kakao_account')
        if not kakao_account:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_email = kakao_account.get('email')

        # token 상세 정보 id, expires_in, app_id
        token_detail_headers = {
            "Authorization": access_token
        }
        token_detail_res = requests.get("https://kapi.kakao.com/v1/user/access_token_info", headers=token_detail_headers)
        token_detail_json = token_detail_res.json()

        res = Response({
            "access token" : access_token,
            "token id" : token_detail_json.get('id'),
            "token expires in" : token_detail_json.get('expires_in'),
            "token app id" : token_detail_json.get('app_id'),

            "user_unique_id": social_id,

            "kakao_account" : kakao_account
        })

        # 회원가입 및 로그인
        res = login_api(social_id=social_id, email=user_email)

        return res
    
class MyPage(APIView):
    def get(self, request):
        user = get_object_or_404(User, userId=request.user.userId)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class MyReports(APIView):
    def get(self, request):
        reports = Report.objects.filter(userId=request.user)
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)

class ReportDetail(APIView):
    def get(self, request, reportId):
        report = get_object_or_404(Report, reportId=reportId, userId=request.user)
        serializer = ReportSerializer(report)
        return Response(serializer.data)

class ChangeUserType(APIView):
    def put(self, request):
        user = get_object_or_404(User, userId=request.user.userId)
        user.userType = request.data.get('userType', user.userType)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)

class ChangeAlarmOption(APIView):
    def put(self, request):
        user = get_object_or_404(User, userId=request.user.userId)
        user.option = request.data.get('option', user.option)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
