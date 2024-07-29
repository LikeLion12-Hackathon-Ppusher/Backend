from django.shortcuts import get_object_or_404
from .serializers import ReportSerializer
from .models import Report
from place.models import Place, SmokingPlace, SecondhandSmokingPlace
from accounts.models import User  # Import the User model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

class PlaceReport(APIView):
    @transaction.atomic
    def post(self, request, format=None):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            try:
                report = serializer.save()
                report_type = report.reportType
                if report_type == 'SM':
                    SmokingPlace.objects.create(placeId=report.placeId, rate='1', ashtray=False)  # Add default values for required fields
                    message = "흡연구역이 성공적으로 제보되었습니다."
                elif report_type == 'SH':
                    SecondhandSmokingPlace.objects.create(placeId=report.placeId)
                    message = "간접 흡연구역이 성공적으로 제보되었습니다."
                else:
                    message = "알 수 없는 보고 유형입니다."

                return Response(
                    {
                        "reportId": report.reportId,
                        "placeId": report.placeId.placeId,
                        "userId": report.userId.userId,
                        "description": report.description,
                        "reportType": report.reportType,
                        "message": message,
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
