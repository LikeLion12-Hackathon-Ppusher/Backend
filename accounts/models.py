from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):

    USER_TYPE = (
        ('SY','흡연자'),
        ('SN','비흡연자')
    )

    DISTANCE = (
        (0,'10M'),
        (1,'20M'),
        (2,'30M')
    )

    GENDER = (
        ('M', '남자'),
        ('F', '여자')
    )

    TIME = (
        (0 ,'즉시'),
        (1 ,'5분'),
        (2, '10분')
    )
    id = models.AutoField(primary_key=True)
    userId = models.CharField(unique=True, max_length=20)
    userType = models.CharField(choices=USER_TYPE, max_length=2)
    kakaoEmail = models.EmailField(unique=True)
    name = models.CharField(max_length=10)
    gender = models.CharField(choices=GENDER, max_length=1)
    distance = models.IntegerField(choices=DISTANCE, null=True, default=0)
    time = models.IntegerField(choices=TIME ,null=True, default=0)
    option = models.BooleanField(default=False)

    USERNAME_FIELD = 'userId'

    class Meta:
        db_table = 'accounts_user'

    @staticmethod
    def get_user_or_none_by_userId(userId):
        try:
            user = User.objects.get(userId=userId)
            return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user_or_none_by_userEmail(email):
        try:
            user = User.objects.get(kakaoEmail=email)
            return user
        except User.DoesNotExist:
            return None