from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # path('place/', include('place.urls')),
    # path('report', include('report.urls')),
    path('oauth/', include('accounts.urls')),
]
