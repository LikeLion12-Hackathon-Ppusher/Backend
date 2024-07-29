from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('place/', include('place.urls')),
    path('report', include('report.urls')),
    path('user/', include('accounts.urls')),
]
