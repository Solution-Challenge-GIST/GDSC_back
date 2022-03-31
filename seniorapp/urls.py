from django.urls import path

from seniorapp.views import SeniorViewSet

urlpatterns = [
    # Junior Profile
    path('', SeniorViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('<int:senior_id>', SeniorViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    # path('me', SeniorViewSet.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update'})),
]