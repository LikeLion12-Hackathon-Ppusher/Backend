from django.shortcuts import get_object_or_404, render
from .serializers import *
from .models import ReportSmokingPlace, SmokingPlace, NoSmokingPlace, SecondhandSmokingPlace

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

####
class ReportSmokingPlaceList(APIView):
    # Create a place
    def post(self, request, format=None):
        serializer = ReportSmokingPlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Get all places
    def get(self, request, format=None):
        reportSmokingplaces = ReportSmokingPlace.objects.all()
        # To serialize many posts, use (many=True)
        serializer = ReportSmokingPlaceSerializer(reportSmokingplaces, many=True)
        return Response(serializer.data)

class ReportSmokingPlaceDetail(APIView):
    def get(self, request, id):
        place = get_object_or_404(ReportSmokingPlace, placeId=id)
        serializer = ReportSmokingPlaceSerializer(place)
        return Response(serializer.data)
    
#####
class SmokingPlaceList(APIView):
    # Create a place
    def post(self, request, format=None):
        serializer = SmokingPlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Get all places
    def get(self, request, format=None):
        smokingplaces = SmokingPlace.objects.all()
        # To serialize many posts, use (many=True)
        serializer = SmokingPlaceSerializer(smokingplaces, many=True)
        return Response(serializer.data)

class SmokingPlaceDetail(APIView):
    def get(self, request, id):
        place = get_object_or_404(SmokingPlace, placeId=id)
        serializer = SmokingPlaceSerializer(place)
        return Response(serializer.data)
    

class NoSmokingPlaceList(APIView):
    # Create a place
    def post(self, request, format=None):
        serializer = NoSmokingPlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Get all places
    def get(self, request, format=None):
        places = NoSmokingPlace.objects.all()
        # To serialize many posts, use (many=True)
        serializer = NoSmokingPlaceSerializer(places, many=True)
        return Response(serializer.data)

class NoSmokingPlaceDetail(APIView):
    def get(self, request, id):
        place = get_object_or_404(NoSmokingPlace, placeId=id)
        serializer = NoSmokingPlaceSerializer(place)
        return Response(serializer.data)
    
    def put(self, request, id):
        place = get_object_or_404(NoSmokingPlace, placeId=id)
        serializer = NoSmokingPlaceSerializer(place, data=request.data)
        if serializer.is_valid():  # Validation is necessary for update
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        place = get_object_or_404(NoSmokingPlace, placeId=id)
        place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SecondhandSmokingPlaceList(APIView):
    # Create a place
    def post(self, request, format=None):
        serializer = SecondhandSmokingPlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Get all places
    def get(self, request, format=None):
        places = SecondhandSmokingPlace.objects.all()
        # To serialize many posts, use (many=True)
        serializer = SecondhandSmokingPlaceSerializer(places, many=True)
        return Response(serializer.data)

class SecondhandSmokingPlaceDetail(APIView):
    def get(self, request, id):
        place = get_object_or_404(SecondhandSmokingPlace, placeId=id)
        serializer = SecondhandSmokingPlaceSerializer(place)
        return Response(serializer.data)
    
    def put(self, request, id):
        place = get_object_or_404(SecondhandSmokingPlace, placeId=id)
        serializer = SecondhandSmokingPlaceSerializer(place, data=request.data)
        if serializer.is_valid():  # Validation is necessary for update
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        place = get_object_or_404(SecondhandSmokingPlace, placeId=id)
        place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SecondhandSmokingPlaceLikes(APIView):
    def post(self, request, id):
        like = Likes.objects.filter(SecondHandSmokingPlaceId = id, userId = request.user).exists()
        # 만약 이미 해당 like 객체에 해당 장소에 대해 userId가 있다면 제거하고, 없다면 추가함
        if like is False:
            # 생성
            likeplace = SecondhandSmokingPlace.objects.get(placeId = id)
            likeplace.likesCount += 1

            like = Likes.objects.create(
                SecondHandSmokingPlaceId = likeplace,
                userId = request.user
            )
            likesSerializer = LikesSerializer(data=like)
            likesSerializer.is_valid()
            return Response({
                "like" : likesSerializer.validated_data
                }, status=status.HTTP_201_CREATED)
        else:
            likeplace = SecondhandSmokingPlace.objects.get(placeId = id)
            likeplace.likesCount -= 1
            Likes.objects.filter(SecondHandSmokingPlaceId = id, userId = request.user).delete()
            
            return Response(status=status.HTTP_204_NO_CONTENT)

