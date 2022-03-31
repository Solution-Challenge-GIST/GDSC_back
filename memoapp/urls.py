from django.urls import path

from memoapp.views import MemoViewSet

urlpatterns = [
    path('albums/<int:album_id>', MemoViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('<int:memo_id>', MemoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]