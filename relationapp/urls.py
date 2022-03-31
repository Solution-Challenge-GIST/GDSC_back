from django.urls import path

from relationapp.views import RelationViewSet

urlpatterns = [
    # Junior Profile
    path('juniors/me/seniors/<int:senior_id>', RelationViewSet.as_view({'post': 'create', 'delete': 'destroy'})),
    path('seniors/me/juniors', RelationViewSet.as_view({'get': 'list'})),
    path('<int:relation_id>', RelationViewSet.as_view({'get': 'retrieve'})),
    # path('me', JuniorViewSet.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update'})),
]