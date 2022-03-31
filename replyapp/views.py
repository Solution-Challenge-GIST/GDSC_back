import uuid
import datetime

from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from albumapp.models import Album
from replyapp.models import Reply, ReplyVoice
from replyapp.serializers import ReplySerializer, ReplyPostSerializer, UploadReplyVoiceSerializer


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, album_id=None, *args, **kwargs):
        data = request.data
        data.update({"album": album_id, "user": request.user.id})

        serializer = ReplyPostSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            reply_id = self.perform_create(serializer)
        except ValidationError as e:
            return Response(e.get_full_details())

        album = get_object_or_404(Album, album_id=album_id)
        album.is_replied = True
        album.save()

        headers = self.get_success_headers(reply_id=reply_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        return instance.reply_id

    def get_success_headers(self, reply_id=None):
        try:
            return {'Location': f"/replies/{reply_id}"}
        except (TypeError, KeyError):
            return {}

    def retrieve(self, request, reply_id=None, *args, **kwargs):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, reply_id=reply_id)

        serializers = self.get_serializer(instance)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def update(self, request, reply_id=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, reply_id=reply_id)
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
        queryset = self.get_queryset().filter(album_id=album_id).order_by('created_date')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, reply_id=None, *args, **kwargs):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, reply_id=reply_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReplyVoiceViewSet(viewsets.ModelViewSet):
    queryset = ReplyVoice.objects.all()
    serializer_class = UploadReplyVoiceSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, album_id=None):
        # validity
        # 용량에 따라 bad request
        VOLUME_10_MB = 10485760
        if len(request.FILES) != 0:
            file = request.FILES['voice']  # 여기서 verification key 값을 가진 게 없을 때 에러 처리 해줘야 함
            ext = str(file).split('.')[-1]
            if file.size > VOLUME_10_MB:
                return Response({"message": "Please upload voice under 10MB"}, status=status.HTTP_400_BAD_REQUEST)
            elif ext not in ['caf', 'm4a', 'flac', 'mp3', 'mp4', 'wav', 'wma', 'aac', 'M4A', 'FLAC', 'MP3', 'MP4', 'WAV', 'WMA', 'AAC', 'CAF']:
                return Response({"message": "Please upload only voices with a proper format"},
                                status=status.HTTP_400_BAD_REQUEST)
            file.name = f'{request.user.email}/{uuid.uuid4().hex}_{datetime.datetime.now()}.{ext}'
            instance = ReplyVoice(voice=file, user=request.user, album_id=album_id)
            instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Please upload at least one voice"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, replyvoice_id=None):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, replyvoice_id=replyvoice_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)