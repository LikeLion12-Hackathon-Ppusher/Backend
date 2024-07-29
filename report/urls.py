from django.contrib import admin
from django.urls import path
from report.views import *


urlpatterns = [
    path('', PlaceReport.as_view()),
]
