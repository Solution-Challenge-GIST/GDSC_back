import uuid
import datetime

from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from simplevoiceapp.models import SimpleVoice, SimpleVoiceFile
from simplevoiceapp.serializers import SimpleVoiceSerializer, SimpleVoicePostSerializer, UploadSimpleVoiceFileSerializer


class SimpleVoiceViewSet(viewsets.ModelViewSet):
    queryset = SimpleVoice.objects.all()
    serializer_class = SimpleVoiceSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, junior_id=None, *args, **kwargs):
        data = request.data
        data.update({"junior": junior_id, "senior": request.user.senior.senior_id})

        serializer = SimpleVoicePostSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            simplevoice_id = self.perform_create(serializer)
        except ValidationError as e:
            return Response(e.get_full_details())

        headers = self.get_success_headers(simplevoice_id=simplevoice_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        return instance.simplevoice_id

    def get_success_headers(self, simplevoice_id=None):
        try:
            return {'Location': f"/simplevoices/{simplevoice_id}"}
        except (TypeError, KeyError):
            return {}

    def retrieve(self, request, simplevoice_id=None, *args, **kwargs):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, simplevoice_id=simplevoice_id)

        serializers = self.get_serializer(instance)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def update(self, request, simplevoice_id=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, simplevoice_id=simplevoice_id)
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
        queryset = self.get_queryset().filter(junior_id=request.user.junior.junior_id).order_by('-created_date')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list_for_senior(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(senior_id=request.user.senior.senior_id).order_by('-created_date')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, simplevoice_id=None, *args, **kwargs):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, simplevoice_id=simplevoice_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SimpleVoiceFileViewSet(viewsets.ModelViewSet):
    queryset = SimpleVoiceFile.objects.all()
    serializer_class = UploadSimpleVoiceFileSerializer
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
            instance = SimpleVoiceFile(voice=file, senior=request.user.senior)
            instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Please upload at least one voice"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, simplevoicefile_id=None):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, simplevoicefile_id=simplevoicefile_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)