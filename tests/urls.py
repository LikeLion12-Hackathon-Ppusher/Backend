from django.urls import path
from tests.views import *

urlpatterns = [
    path('test/', hello_world_test, name = 'hello_world_test'),
    path('connect/', connections_test, name = "connection_test"),

    path('list/', PostList.as_view()),
    path('<int:id>/', PostDetail.as_view())
]