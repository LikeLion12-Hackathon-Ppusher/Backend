from django.contrib import admin
from django.urls import path
from place.views import *


urlpatterns = [
    path('smoking', SmokingPlaceList.as_view()),
    path('smoking/<id>', SmokingPlaceDetail.as_view()),
    path('nosmoking', NoSmokingPlaceList.as_view()),
    path('nosmoking/<id>', SmokingPlaceDetail.as_view()),
    path('shsmoking', SecondhandSmokingPlaceList.as_view()),
    path('shsmoking/likes', SecondhandSmokingPlaceLikes.as_view()),
    path('shsmoking/<id>',SecondhandSmokingPlaceDetail.as_view()),
]
