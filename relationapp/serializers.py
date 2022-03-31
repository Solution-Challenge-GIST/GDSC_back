from rest_framework import serializers

from juniorapp.serializers import JuniorSerializer
from relationapp.models import Relation


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = '__all__'


class RelationListSerializer(serializers.ModelSerializer):
    junior = JuniorSerializer()

    class Meta:
        model = Relation
        fields = ['relation_id', 'junior', 'relation']