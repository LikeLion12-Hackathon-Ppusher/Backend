###Model Serializer case
from rest_framework import serializers
from .models import *

# class PlaceSerializer(serializers.ModelSerializer):

#     class Meta:
#             # 어떤 모델을 시리얼라이즈할 건지
#         model = Place
#             # 모델에서 어떤 필드를 가져올지
#             # 전부 가져오고 싶을 때
#         fields = "__all__"
        
        
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

    def create(self, validated_data):
        place_data = validated_data.pop('place')
        place = Place.objects.create(**place_data)
        nosmokingplace = NoSmokingPlace.objects.create(place=place, **validated_data)
        return nosmokingplace
        
class SecondhandSmokingPlaceSerializer(serializers.ModelSerializer):

    class Meta:
            # 어떤 모델을 시리얼라이즈할 건지
        model = SecondhandSmokingPlace
            # 모델에서 어떤 필드를 가져올지
            # 전부 가져오고 싶을 때
