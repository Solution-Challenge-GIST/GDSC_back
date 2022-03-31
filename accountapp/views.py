from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from accountapp.models import User
from accountapp.serializers import JuniorUserSerializer, UserSerializer, SeniorUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        user_id = request.user.id
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, id=user_id)
        if request.user.role == 'JUNIOR':
            serializer = JuniorUserSerializer(instance)
        # elif request.user.role == 'SENIOR':
            # serializer = SeniorUserSerializer(instance)
        elif request.user.role == 'SENIOR':
            serializer = SeniorUserSerializer(instance)
        else:
            serializer = UserSerializer(instance)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user_id = request.user.id
        instance = get_object_or_404(queryset, id=user_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)