from rest_framework import serializers

import datetime

from juniorapp.serializers import JuniorSerializer
from seniorapp.serializers import SeniorSerializer
from simplevoiceapp.models import SimpleVoice, SimpleVoiceFile


class SimpleVoiceSerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField()
    senior = SeniorSerializer()
    junior = JuniorSerializer()

    def get_day(self, obj):
        return datetime.datetime.weekday(obj.created_date)

    class Meta:
        model = SimpleVoice
        fields = '__all__'


class SimpleVoicePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleVoice
        fields = '__all__'


class UploadSimpleVoiceFileSerializer(serializers.ModelSerializer):
    voice = serializers.FileField()

    class Meta:
        model = SimpleVoiceFile
        exclude = ['senior']