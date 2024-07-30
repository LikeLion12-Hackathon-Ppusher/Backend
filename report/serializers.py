from rest_framework import serializers
from .models import Report
from place.models import *
from place.serializers import SmokingPlaceSerializer, SecondhandSmokingPlaceSerializer

class ReportSerializer(serializers.ModelSerializer):
    smokingPlace = SmokingPlaceSerializer(required=False)
    secondhandSmokingPlace = SecondhandSmokingPlaceSerializer(required=False)

    class Meta:
        model = Report
        fields = ['reportId', 'smokingPlace', 'secondhandSmokingPlace', 'userId', 'description', 'reportType']

    def validate(self, data):
        if data['reportType'] == 'SM':
            if 'smokingPlace' not in data:
                raise serializers.ValidationError("흡연 구역 제보에는 'smokingPlace' 데이터가 필요합니다.")
        elif data['reportType'] == 'SH':
            if 'secondhandSmokingPlace' not in data:
                raise serializers.ValidationError("간접 흡연 구역 제보에는 'secondhandSmokingPlace' 데이터가 필요합니다.")
        return data

    def create(self, validated_data):
        report_type = validated_data.get('reportType')

        if report_type == 'SM':
            place_data = validated_data.pop('smokingPlace')
            place = SmokingPlace.objects.create(**place_data)
            validated_data['smokingPlace'] = place
        elif report_type == 'SH':
            place_data = validated_data.pop('secondhandSmokingPlace')
            place = SecondhandSmokingPlace.objects.create(**place_data)
            validated_data['secondhandSmokingPlace'] = place

        return Report.objects.create(**validated_data)
