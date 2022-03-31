from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from relationapp.models import Relation
from relationapp.serializers import RelationSerializer, RelationListSerializer


class RelationViewSet(viewsets.ModelViewSet):
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer
    permission_classes = [permissions.AllowAny]

    # POST : /juniors/me/seniors/1/relation
    # Body : {"relation" : "딸"}
    def create(self, request, senior_id=None, *args, **kwargs):
        if self.get_queryset().filter(junior_id=request.user.junior.junior_id, senior_id=senior_id).exists():
            return self.update(request, senior_id)
        data = request.data
        data.update({"senior": senior_id, "junior": request.user.junior.junior_id})

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            relation_id = self.perform_create(serializer)
        except ValidationError as e:
            return Response(e.get_full_details())
        headers = self.get_success_headers(relation_id=relation_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        return instance.relation_id

    def get_success_headers(self, relation_id=None):
        try:
            return {'Location': f"/relations/{relation_id}"}
        except (TypeError, KeyError):
            return {}

    def retrieve(self, request, relation_id=None, *args, **kwargs):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, relation_id=relation_id)

        serializers = self.get_serializer(instance)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    # seniors/me/juniors
    def list(self, request,  *args, **kwargs):
        queryset = self.get_queryset().filter(senior_id=request.user.senior.senior_id)
        serializer = RelationListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, senior_id=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, senior_id=senior_id, junior_id=request.user.junior.junior_id)
        data = request.data
        data.update({"senior": senior_id, "junior": request.user.junior.junior_id})
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

    # juniors/me/seniors/1
    def destroy(self, request, senior_id=None, *args, **kwargs):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, senior_id=senior_id, junior_id=request.user.junior.junior_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

