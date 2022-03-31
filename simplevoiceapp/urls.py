from django.urls import path

from simplevoiceapp.views import SimpleVoiceViewSet, SimpleVoiceFileViewSet

urlpatterns = [
    # Reply
    path('seniors/me/juniors/<int:junior_id>', SimpleVoiceViewSet.as_view({'post': 'create'})),

    path('seniors/me', SimpleVoiceViewSet.as_view({'get': 'list_for_senior'})),
    path('juniors/me', SimpleVoiceViewSet.as_view({'get': 'list_for_junior'})),

    path('<int:simplevoice_id>', SimpleVoiceViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),

    # File Upload
    path('files', SimpleVoiceFileViewSet.as_view({'post': 'create'})),
]