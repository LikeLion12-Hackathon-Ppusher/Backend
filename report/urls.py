from django.contrib import admin
from django.urls import path
from report.views import *


urlpatterns = [
    path('smokingplace', SmokingPlaceReport.as_view()),
    path('shsmokingplace', SecondHandSmokingPlaceReport.as_view()),
]
