from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.serializers import RefreshToken
from django.contrib.auth import logout
from .models import User
from .serializers import UserSerializer, RegisterSerializer, AuthSerializer
from report.serializers import ReportSerializer
from report.models import Report
from place.models import SecondhandSmokingPlace, ReportSmokingPlace, Likes
from config.settings import KAKAO_CONFIG
import requests

# Kakao 관련 URI
kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"

class UserView(APIView):
    permission_classes = [AllowAny]

    def create_user(self, data):
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        return Response(
            {
                "user": serializer.data,
                "message": "register success",
                "token": {
                    "access_token": str(token.access_token),
                    "refresh_token": str(token),
                },
            },
            status=status.HTTP_201_CREATED,
        )

    def post(self, request):
        return self.create_user(data=request.data)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def authenticate_user(self, data):
        serializer = AuthSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response(
            {
                "user": {
                    "userId": user.id,
                    "userName": user.name,
                    "userType": user.userType,
                },
                "setting": {
                    "distance": user.distance,
                    "time": user.time,
                    "option": user.option,
                },
                "message": "login success",
                "access_token": serializer.validated_data["access_token"],
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        return self.authenticate_user(data=request.data)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK)

def login_api(social_id: str, email: str = None, name: str = None):
    user = User.get_user_or_none_by_userId(userId=social_id)
    userbyemail = User.get_user_or_none_by_userEmail(email=email)
    login_view = LoginView()
    if user:
        data = {'userId': social_id, 'kakaoEmail': email, "name": name}
        response = login_view.authenticate_user(data=data)
    else:
        data = {'userId': social_id, 'kakaoEmail': email, "name" : name}
        user_view = UserView()
        user_creation_response = user_view.create_user(data=data)
        response = login_view.authenticate_user(data=data)
        response.status_code = 201
    return response

class KakaoLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        client_id = KAKAO_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = KAKAO_CONFIG['KAKAO_REDIRECT_URI']
        uri = f"{kakao_login_uri}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        return redirect(uri)

class KakaoCallbackView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get("authorizationCode")
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        token_response = requests.post(
            kakao_token_uri,
            data={
                'grant_type': 'authorization_code',
                'client_id': KAKAO_CONFIG['KAKAO_REST_API_KEY'],
                'redirect_uri': KAKAO_CONFIG['KAKAO_REDIRECT_URI'],
                'client_secret': KAKAO_CONFIG['KAKAO_CLIENT_SECRET_KEY'],
                'code': code,
            },
            headers={'Content-type': 'application/x-www-form-urlencoded'},
        ).json()

        access_token = token_response.get('access_token')
        if not access_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user_info_response = requests.get(
            kakao_profile_uri,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            },
        ).json()

        social_id = f"kakao_{user_info_response.get('id')}"
        user_email = user_info_response.get('kakao_account', {}).get('email')
        user_name =  user_info_response.get('kakao_account', {}).get('name')
        return login_api(social_id=social_id, email=user_email, name = user_name)

class MyPage(APIView):
    def get(self, request):
        user = get_object_or_404(User, userId=request.user)
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

    def delete(self, request, reportId):
            report_id = reportId
            if not report_id:
                return Response({"error": "Report ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                report = Report.objects.get(reportId=report_id, userId=request.user.id)
                if report.reportSmokingPlace:
                    place = ReportSmokingPlace.objects.get(placeId = report.reportSmokingPlace.placeId)
                elif report.secondhandSmokingPlace:
                    place = SecondhandSmokingPlace.objects.get(placeId = report.secondhandSmokingPlace.placeId)
                    likes = Likes.objects.get(userId = request.user.id, SecondHandSmokingPlaceId = report.secondhandSmokingPlace.placeId)
                
                place.delete()

                return Response({"message": "Report has been successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
            except Report.DoesNotExist:
                return Response({"error": "Report not found or you do not have permission to delete this report."}, status=status.HTTP_404_NOT_FOUND)

class ChangeUserType(APIView):
    def put(self, request):
        user = get_object_or_404(User, userId=request.user)
        user.userType = request.data.get('userType', user.userType)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)

class ChangeAlarmOption(APIView):
    def put(self, request):
        user = get_object_or_404(User, userId=request.user)
        user.option = request.data.get('option', user.option)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)

class ChangeAlarmTime(APIView):
    def put(self, request):
        user = get_object_or_404(User, userId=request.user)
        user.time = request.data.get('time', user.time)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
        
class ChangeAlarmDistance(APIView):
    def put(self, request):
        user = get_object_or_404(User, userId=request.user)
        user.distance = request.data.get('distance', user.distance)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
