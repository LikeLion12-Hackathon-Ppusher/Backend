from django.shortcuts import render, redirect

from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, AuthSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import logout

class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save(request)
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

class AuthView(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]
            res = Response(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                    },
                    "message": "login success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access-token", access_token, httponly=True)
            res.set_cookie("refresh-token", refresh_token, httponly=True)
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK)

kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"

from config.settings import *
from .models import User
import requests

def login_api(social_type: str, social_id: str, email: str=None, phone: str=None):
    '''
    회원가입 및 로그인
    '''
    login_view = AuthView()
    try:
        User.objects.get(social_id=social_id)
        data = {
            'social_id': social_id,
            'email': email,
        }
        response = login_view.object(data=data)

    except User.DoesNotExist:
        data = {
            'social_type': social_type,
            'social_id': social_id,
            'email': email,
        }
        user_view = AuthView()
        login = user_view.get_or_create_user(data=data)

        response = login_view.object(data=data) if login.status_code == 201 else login

    return response


class KakaoLoginView(APIView):
    permission_classes = [AllowAny,]

    def get(self, request):
        '''
        kakao code 요청

        ---
        '''
        client_id = KAKAO_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = KAKAO_CONFIG['KAKAO_REDIRECT_URI']
        uri = f"{kakao_login_uri}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        
        res = redirect(uri)
        return res
    
class KakaoCallbackView(APIView):
    permission_classes = [AllowAny]

    # @swagger_auto_schema(query_serializer=CallbackUserInfoSerializer)
    def get(self, request):
        '''
        kakao access_token 및 user_info 요청

        ---
        '''
        data = request.query_params

        # access_token 발급 요청
        code = data.get('code')
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
        print(request_data)
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        token_res = requests.post(kakao_token_uri, data=request_data, headers=token_headers)

        token_json = token_res.json()
        access_token = token_json.get('access_token')

        if not access_token:
            print("access_token error")
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
            print("kakao_account error")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_email = kakao_account.get('email')

        # 회원가입 및 로그인
        # res = login_api(social_type=social_type, social_id=social_id, email=user_email)
        res = Response({
            "access token" : access_token
        })
        return res
