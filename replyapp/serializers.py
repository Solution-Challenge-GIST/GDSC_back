from django.shortcuts import get_object_or_404
from rest_framework import serializers

from juniorapp.models import Junior
from juniorapp.serializers import JuniorSerializer
from replyapp.models import Reply, ReplyVoice
import datetime

from seniorapp.models import Senior
from seniorapp.serializers import SeniorSerializer


class ReplySerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField()
    replier = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    def get_day(self, obj):
        return datetime.datetime.weekday(obj.created_date)

    def get_replier(self, obj):
        if obj.user.role == 'JUNIOR':
            replier = get_object_or_404(Junior, junior_id=obj.user.junior.junior_id)
            return JuniorSerializer(replier).data
        elif obj.user.role == 'SENIOR':
            replier = get_object_or_404(Senior, senior_id=obj.user.senior.senior_id)
            return SeniorSerializer(replier).data
        else:
            return None

    def get_role(self, obj):
        if obj.user.role == 'JUNIOR':
            return 'JUNIOR'
        elif obj.user.role == 'SENIOR':
            return 'SENIOR'
        else:
            return ''

    class Meta:
        model = Reply
        exclude = ['album']


class ReplyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'


class UploadReplyVoiceSerializer(serializers.ModelSerializer):
    voice = serializers.FileField()

    class Meta:
        model = ReplyVoice
        exclude = ['user', 'album']