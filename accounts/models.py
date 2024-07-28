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

    userId = models.AutoField(primary_key=True)
    userType = models.CharField(choices=USER_TYPE, max_length=2)
    kakaoEmail = models.EmailField(unique=True)
    name = models.CharField(max_length=10)
    gender = models.CharField(choices=GENDER, max_length=1)
    distance = models.IntegerField(choices=DISTANCE, null=True)
    time = models.IntegerField(choices=TIME ,null=True)
    option = models.BooleanField(default=False)

    USERNAME_FIELD = 'kakaoEmail'

    @staticmethod
    def get_user_or_none_by_email(kakao_email):
        try:
            return User.objects.get(kakao_email=kakao_email)
        except Exception:
            return None