import datetime
import os

from rest_framework import serializers

from albumapp.models import Album, AlbumVoice, AlbumImage
from juniorapp.serializers import JuniorSerializer
from memoapp.models import Memo
from memoapp.serializers import MemoSerializerForAlbum
from seniorapp.serializers import SeniorSerializer


class AlbumSerializer(serializers.ModelSerializer):
    junior = JuniorSerializer()
    senior = SeniorSerializer()

    day = serializers.SerializerMethodField()

    def get_day(self, obj):
        return datetime.datetime.weekday(obj.created_date)

    class Meta:
        model = Album
        fields = '__all__'


class AlbumListSerializer(serializers.ModelSerializer):
    junior = JuniorSerializer()
    senior = SeniorSerializer()
    memo = serializers.SerializerMethodField()

    day = serializers.SerializerMethodField()

    def get_day(self, obj):
        return datetime.datetime.weekday(obj.created_date)

    def get_memo(self, obj):
        memo = Memo.objects.filter(album_id=obj.album_id).first()

        return MemoSerializerForAlbum(memo).data

    class Meta:
        model = Album
        fields = '__all__'


class AlbumPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'


class UploadAlbumVoiceSerializer(serializers.ModelSerializer):
    voice = serializers.FileField()

    class Meta:
        model = AlbumVoice
        exclude = ['user']


class UploadAlbumImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = AlbumImage
        exclude = ['user']
