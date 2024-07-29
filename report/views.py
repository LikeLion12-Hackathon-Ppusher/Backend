from django.shortcuts import get_object_or_404, render
from .serializers import *
from .models import SmokingPlace, NoSmokingPlace, SecondhandSmokingPlace

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class SmokingPlaceReport(APIView):
    # 흡연 구역 제보
    def post(self, request, format=None):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SecondHandSmokingPlaceReport(APIView):
    # 간접 흡연 구역 제보
    def post(self, request, format=None):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)