from django.contrib import admin
from django.urls import path
from place.views import *


urlpatterns = [
    path('smoking', SmokingPlaceList.as_view()),
    path('smoking/<int:id>', SmokingPlaceDetail.as_view()),
    path('nosmoking', NoSmokingPlaceList.as_view()),
    path('nosmoking/<int:id>', SmokingPlaceDetail.as_view()),
    path('shsmoking', SecondhandSmokingPlaceList.as_view()),
    path('shsmoking/<int:id>/likes', SecondhandSmokingPlaceLikes.as_view()),
    path('shsmoking/<int:id>',SecondhandSmokingPlaceDetail.as_view()),
]
