from rest_framework import serializers

from juniorapp.models import Junior
from juniorapp.serializers import JuniorSerializer
from memoapp.models import Memo


class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = '__all__'


class MemoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = '__all__'


class MemoSerializerForAlbum(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = ['memo_id', 'title', 'content', 'emotion', 'created_date', 'junior']
