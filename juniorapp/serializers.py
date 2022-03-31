from rest_framework import serializers

from juniorapp.models import Junior


class JuniorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Junior
        fields = '__all__'