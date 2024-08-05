# accounts/serializers.py
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(required=True)
    # name = serializers.CharField(required=True)
    # userType = serializers.CharField(required=True)
    kakaoEmail = serializers.CharField(required=True)
    # gender = serializers.CharField(required=True)


    class Meta:
        model = User
        fields = ['userId','kakaoEmail']
        # fields = ['userId', 'name', 'kakaoEmail', 'userType', 'gender']

    def create(self, validated_data):
        user = User.objects.create(
            userId=self.validated_data['userId'],
            name=self.validated_data['user'].name,
            userType='SY',
            kakaoEmail=self.validated_data['kakaoEmail'],
            distance = 2,
            gender='M'
        )

        return user
        
    def validate(self, data):
        userId = data.get('userId',None)
        # userType = data.get('userType',None)
        # gender = data.get('gender',None)

        if User.objects.filter(userId=userId).exists():
            raise serializers.ValidationError('userId already exists')
        # if gender not in ('M', 'F'):
        #     raise serializers.ValidationError('user gender error')
        # if userType not in ('SY', 'SN'):
        #     raise serializers.ValidationError('user type error')

        return data

class AuthSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['userId']
    
    def validate(self, data):

        userId = data.get("userId", None)

        user = User.get_user_or_none_by_userId(userId=userId)

        if user is None:
            raise serializers.ValidationError("user account not exist")

        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            "user": user,
            "refresh_token": refresh_token,
            "access_token": access_token,
        }

        return data
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'