from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from seniorapp.models import Senior
from seniorapp.serializers import SeniorSerializer


class SeniorViewSet(viewsets.ModelViewSet):
    queryset = Senior.objects.all()
    serializer_class = SeniorSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data
        data.update({"user": request.user.id})

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            senior_id = self.perform_create(serializer)
        except ValidationError as e:
            return Response(e.get_full_details())
        headers = self.get_success_headers(senior_id=senior_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, user_pk=None):
        instance = serializer.save()
        return instance.id

    def get_success_headers(self, senior_id):
        try:
            return {'Location': f"/seniors/{senior_id}"}
        except (TypeError, KeyError):
            return {}

    def retrieve(self, request, senior_id=None, *args, **kwargs):
        queryset = self.get_queryset()
        profile = get_object_or_404(queryset, senior_id=senior_id)

        serializers = self.get_serializer(profile)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def update(self, request, senior_id=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, senior_id=senior_id)
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

    def list(self, request, dev_pk=None, *args, **kwargs):
        queryset = self.get_queryset().order_by('name')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)