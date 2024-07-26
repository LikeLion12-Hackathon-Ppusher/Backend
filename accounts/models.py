from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass #해당 세션에서 바로 유저모델을 사용할 것은 아니기 때문에 pass로 넣겠습니다.

    @staticmethod
    def get_user_or_none_by_username(username):
        # 왜 try-exception? -> get은 error를 반환! filter는 None을 반환~
        try:
            return User.objects.get(username=username)
        except Exception:
            return None

    # 얘가 추가된게 중요하다고 하네요~
    @staticmethod
    def get_user_or_none_by_email(email):
        try:
            return User.objects.get(email=email)
        except Exception:
            return None