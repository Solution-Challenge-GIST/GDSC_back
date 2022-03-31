from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from memoapp.models import Memo
from memoapp.serializers import MemoSerializer, MemoPostSerializer


class MemoViewSet(viewsets.ModelViewSet):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, album_id=None, *args, **kwargs):
        data = request.data
        data.update({"album": album_id, "junior": request.user.junior.junior_id})

        serializer = MemoPostSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            memo_id = self.perform_create(serializer)
        except ValidationError as e:
            return Response(e.get_full_details())
        headers = self.get_success_headers(memo_id=memo_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        return instance.memo_id

    def get_success_headers(self, memo_id=None):
        try:
            return {'Location': f"/memos/{memo_id}"}
        except (TypeError, KeyError):
            return {}

    def retrieve(self, request, memo_id=None, *args, **kwargs):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, memo_id=memo_id)

        serializers = self.get_serializer(instance)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def update(self, request, memo_id=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, memo_id=memo_id)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
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

    def list(self, request, album_id=None, *args, **kwargs):
        queryset = self.get_queryset().filter(album_id=album_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, memo_id=None, *args, **kwargs):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, memo_id=memo_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)