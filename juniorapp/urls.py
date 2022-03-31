from django.urls import path

from juniorapp.views import JuniorViewSet

urlpatterns = [
    # Junior Profile
    path('', JuniorViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('<int:junior_id>', JuniorViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    # path('me', JuniorViewSet.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update'})),
]