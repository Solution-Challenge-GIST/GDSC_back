from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from accountapp.models import User
from juniorapp.models import Junior
from juniorapp.serializers import JuniorSerializer


class JuniorViewSet(viewsets.ModelViewSet):
    queryset = Junior.objects.all()
    serializer_class = JuniorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        data.update({"user": request.user.id})

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            junior_id = self.perform_create(serializer)
        except ValidationError as e:
            return Response(e.get_full_details())
        headers = self.get_success_headers(junior_id=junior_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, user_pk=None):
        instance = serializer.save()
        return instance.id

    def get_success_headers(self, junior_id):
        try:
            return {'Location': f"/juniors/{junior_id}"}
        except (TypeError, KeyError):
            return {}

    def retrieve(self, request, junior_id=None, *args, **kwargs):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, junior_id=junior_id)

        serializers = self.get_serializer(instance)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def update(self, request, junior_id=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, junior_id=junior_id)
        data = request.data
        data.update({"user": request.user.id})
        serializer = self.get_serializer(instance, data=data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except ValidationError as e:
            return Response(e.get_full_details())

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('name')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)