from django.urls import path

from replyapp.views import ReplyViewSet

urlpatterns = [
    # Reply
    path('<int:reply_id>', ReplyViewSet.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'})),
]