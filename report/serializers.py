from rest_framework import serializers
from .models import Report
from place.models import ReportSmokingPlace, SecondhandSmokingPlace, Likes
from place.serializers import ReportSmokingPlaceSerializer, SecondhandSmokingPlaceSerializer

class ReportSerializer(serializers.ModelSerializer):
    reportSmokingPlace = ReportSmokingPlaceSerializer(required=False)
    secondhandSmokingPlace = SecondhandSmokingPlaceSerializer(required=False)

    class Meta:
        model = Report
        fields = ['reportId', 'reportSmokingPlace', 'secondhandSmokingPlace', 'userId', 'description', 'reportType']

    def create(self, validated_data):
        report_type = validated_data.get('reportType')

        if report_type == 'SM':
            place_data = validated_data.pop('reportSmokingPlace', None)
            if place_data:
                place = ReportSmokingPlace.objects.create(**place_data)
                validated_data['reportSmokingPlace'] = place
        elif report_type == 'SH':
            place_data = validated_data.pop('secondhandSmokingPlace', None)
            if place_data:
                place = SecondhandSmokingPlace.objects.create(**place_data)

                like = Likes.objects.create(**{"SecondHandSmokingPlaceId":place, "userId":validated_data["userId"]})
                validated_data['secondhandSmokingPlace'] = place
                validated_data['likesId'] = like

        return Report.objects.create(**validated_data)
