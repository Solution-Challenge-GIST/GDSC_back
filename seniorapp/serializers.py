from rest_framework import serializers

from seniorapp.models import Senior


class SeniorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Senior
        fields = '__all__'