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

        def create(self, validated_data):
            report_type = validated_data.get('reportType')

            if report_type == 'SM':
                place_id = validated_data.pop('smokingPlace', None)
                if place_id:
                    place = SmokingPlace.objects.get(id=place_id['id'])
                    validated_data['smokingPlace'] = place
            elif report_type == 'SH':
                place_id = validated_data.pop('secondhandSmokingPlace', None)
                if place_id:
                    place = SecondhandSmokingPlace.objects.get(id=place_id['id'])
                    validated_data['secondhandSmokingPlace'] = place

            return Report.objects.create(**validated_data)
