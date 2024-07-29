###Model Serializer case
from rest_framework import serializers
from .models import *

class PlaceSerializer(serializers.ModelSerializer):

    class Meta:
            # 어떤 모델을 시리얼라이즈할 건지
        model = Place
            # 모델에서 어떤 필드를 가져올지
            # 전부 가져오고 싶을 때
        fields = "__all__"
        
        
class SmokingPlaceSerializer(serializers.ModelSerializer):

    class Meta:
            # 어떤 모델을 시리얼라이즈할 건지
        model = SmokingPlace
            # 모델에서 어떤 필드를 가져올지
            # 전부 가져오고 싶을 때
        fields = "__all__"
        
class NoSmokingPlaceSerializer(serializers.ModelSerializer):

    class Meta:
            # 어떤 모델을 시리얼라이즈할 건지
        model = NoSmokingPlace
            # 모델에서 어떤 필드를 가져올지
            # 전부 가져오고 싶을 때
        fields = "__all__"
        
class SecondhandSmokingPlaceSerializer(serializers.ModelSerializer):

    class Meta:
            # 어떤 모델을 시리얼라이즈할 건지
        model = SecondhandSmokingPlace
            # 모델에서 어떤 필드를 가져올지
            # 전부 가져오고 싶을 때
        fields = "__all__"

class SecondhandSmokingPlaceLikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Likes

        fields = "__all__"
    def validate(self, userId, like):
        # 만약 이미 해당 like 객체에 userId가 있다면 제거하고, 없다면 추가함
        if Likes.objects.get()
