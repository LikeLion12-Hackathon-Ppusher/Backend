from rest_framework import serializers
from .models import Report
from place.models import SmokingPlace, SecondhandSmokingPlace
from place.serializers import SmokingPlaceSerializer, SecondhandSmokingPlaceSerializer

class ReportSerializer(serializers.ModelSerializer):
    smokingPlace = SmokingPlaceSerializer(required=False)
    secondhandSmokingPlace = SecondhandSmokingPlaceSerializer(required=False)

    class Meta:
        model = Report
        fields = ['reportId', 'smokingPlace', 'secondhandSmokingPlace', 'userId', 'description', 'reportType']

    def create(self, validated_data):
        report_type = validated_data.get('reportType')

        if report_type == 'SM':
            place_data = validated_data.pop('smokingPlace', None)
            if place_data:
                place = SmokingPlace.objects.create(**place_data)
                validated_data['smokingPlace'] = place
        elif report_type == 'SH':
            place_data = validated_data.pop('secondhandSmokingPlace', None)
            if place_data:
                place = SecondhandSmokingPlace.objects.create(**place_data)
                validated_data['secondhandSmokingPlace'] = place

        return Report.objects.create(**validated_data)
