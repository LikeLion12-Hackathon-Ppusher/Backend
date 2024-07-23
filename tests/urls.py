from django.urls import path
from tests.views import *

urlpatterns = [
    path('', hello_world_test, name = 'hello_world_test'),
    path('test/', connections_test, name = "connection_test")
]