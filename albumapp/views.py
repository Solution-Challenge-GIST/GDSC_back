import datetime
import uuid

from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.core.files.base import File

from albumapp.models import Album, AlbumImage, AlbumVoice
from albumapp.serializers import AlbumSerializer, AlbumPostSerializer, AlbumListSerializer, UploadAlbumImageSerializer, \
    UploadAlbumVoiceSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, senior_id=None, *args, **kwargs):
        data = request.data
        data.update({"junior": request.user.junior.junior_id, "senior": senior_id})

        serializer = AlbumPostSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            album_id = self.perform_create(serializer)
        except ValidationError as e:
            return Response(e.get_full_details())
        headers = self.get_success_headers(album_id=album_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        return instance.album_id

    def get_success_headers(self, album_id=None):
        try:
            return {'Location': f"/albums/{album_id}"}
        except (TypeError, KeyError):
            return {}

    def retrieve(self, request, album_id=None, *args, **kwargs):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, album_id=album_id)

        serializers = self.get_serializer(instance)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def update(self, request, album_id=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, album_id=album_id)
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

    def list_for_junior(self, request, *args, **kwargs):
        is_replied = request.GET.get("is_replied", None)
        queryset = self.get_queryset().order_by('-created_date')
        if is_replied is None:
            queryset = queryset.filter(junior_id=request.user.junior.junior_id)
        elif is_replied == "0":
            queryset = queryset.filter(junior_id=request.user.junior.junior_id, is_replied=False)
        elif is_replied == "1":
            queryset = queryset.filter(junior_id=request.user.junior.junior_id, is_replied=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AlbumListSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AlbumListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list_for_senior(self, request, *args, **kwargs):
        is_replied = request.GET.get("is_replied", None)
        queryset = self.get_queryset()
        if is_replied is None:
            queryset = queryset.filter(senior_id=request.user.senior.senior_id)
        elif is_replied == "0":
            queryset = queryset.filter(senior_id=request.user.senior.senior_id, is_replied=False)
        elif is_replied == "1":
            queryset = queryset.filter(senior_id=request.user.senior.senior_id, is_replied=True)
        queryset = queryset.order_by('-created_date')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AlbumListSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AlbumListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, album_id=None, *args, **kwargs):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, album_id=album_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AlbumImageViewSet(viewsets.ModelViewSet):
    queryset = AlbumImage.objects.all()
    serializer_class = UploadAlbumImageSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        # validity
        # 용량에 따라 bad request
        VOLUME_50_MB = 52428800
        if len(request.FILES) != 0:
            file = request.FILES['image'] # 여기서 verification key 값을 가진 게 없을 때 에러 처리 해줘야 함
            ext = str(file).split('.')[-1]
            if file.size > VOLUME_50_MB:
                return Response({"message" : "Please upload image under 50MB"}, status=status.HTTP_400_BAD_REQUEST)
            elif ext not in ['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG']:
                return Response({"message" : "Please upload only images with jpg, jpeg or png format"}, status=status.HTTP_400_BAD_REQUEST)
            file.name = f'{request.user.email}/{uuid.uuid4().hex}_{datetime.datetime.now()}.{ext}'
            instance = AlbumImage(image=file, user=request.user)
            instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message" : "Please upload at least one image"}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, albumimage_id=None):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, albumimage_id=albumimage_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AlbumVoiceViewSet(viewsets.ModelViewSet):
    queryset = AlbumVoice.objects.all()
    serializer_class = UploadAlbumVoiceSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
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
            instance = AlbumVoice(voice=file, user=request.user)
            instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Please upload at least one voice"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, albumvoice_id=None):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, albumvoice_id=albumvoice_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

