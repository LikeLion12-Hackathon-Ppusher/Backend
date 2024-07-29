###Model Serializer case
from rest_framework import serializers
from .models import *
from place.serializers import *

class ReportSerializer(serializers.ModelSerializer):
    place = PlaceSerializer()

    class Meta:
        model = Report
        fields = ['reportId', 'place', 'userId', 'description', 'reportType']

    def create(self, validated_data):
        place_data = validated_data.pop('place')
        place = Place.objects.create(**place_data)
        user = validated_data.pop('userId')
        return Report.objects.create(placeId=place, userId=user, **validated_data)