from django.urls import path

from albumapp.views import AlbumViewSet, AlbumImageViewSet, AlbumVoiceViewSet
from replyapp.views import ReplyViewSet, ReplyVoiceViewSet

urlpatterns = [
    # Album Create
    path('juniors/me/seniors/<int:senior_id>', AlbumViewSet.as_view({'post': 'create'})),

    # Album List
    path('juniors/me', AlbumViewSet.as_view({'get': 'list_for_junior'})),
    path('seniors/me', AlbumViewSet.as_view({'get': 'list_for_senior'})),

    path('<int:album_id>', AlbumViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Reply List
    path('<int:album_id>/replies', ReplyViewSet.as_view({'post': 'create', 'get': 'list'})),

    path('<int:album_id>/replyvoices', ReplyVoiceViewSet.as_view({'post': 'create'})),

    # Media
    path('images', AlbumImageViewSet.as_view({'post': 'create'})),
    path('images/<int:albumimage_id>',  AlbumImageViewSet.as_view({'delete': 'destroy'})),

    path('voices', AlbumVoiceViewSet.as_view({'post': 'create'})),
    path('voices/<int:albumvoice_id>',  AlbumVoiceViewSet.as_view({'delete': 'destroy'})),


]