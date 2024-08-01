from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .serializers import ReportSerializer
from .models import Report

class PlaceReport(APIView):
    @transaction.atomic
    def post(self, request, format=None):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            try:
                report = serializer.save()
                message = "제보가 성공적으로 접수되었습니다."

                response_data = {
                    "reportId": report.reportId,
                    "userId": report.userId.id,
                    "description": report.description,
                    "reportType": report.reportType,
                    "message": message,
                }
                
                if report.reportType == 'SM' and report.smokingPlace:
                    response_data["placeId"] = report.smokingPlace.SmokingPlaceId
                elif report.reportType == 'SH' and report.secondhandSmokingPlace:
                    response_data["placeId"] = report.secondhandSmokingPlace.SecondhandSmokingPlaceId

                return Response(response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
