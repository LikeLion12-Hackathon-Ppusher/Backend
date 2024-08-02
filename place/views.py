from django.shortcuts import get_object_or_404, render
from .serializers import *
from .models import SmokingPlace, NoSmokingPlace, SecondhandSmokingPlace

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
    
    def put(self, request, id):
        place = get_object_or_404(SmokingPlace, placeId=id)
        serializer = SmokingPlaceSerializer(place, data=request.data)
        if serializer.is_valid():  # Validation is necessary for update
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        place = get_object_or_404(SmokingPlace, placeId=id)
        place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
        userId = request.data.get("userId",None)
        like = get_object_or_404(Likes, NoSmokingPlaceId = id, userId_id = userId)
        # 만약 이미 해당 like 객체에 해당 장소에 대해 userId가 있다면 제거하고, 없다면 추가함
        if like is None:
            # 생성
            like = Likes.objects.create(
                NoSmokingPlaceId_id = id,
                userId_id = userId
            )
            return Response({
                "like" : like
                }, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

