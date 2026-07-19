from rest_framework import serializers
from .models import Child


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ('id', 'name', 'surname', 'grade', 'school', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ChildCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ('name', 'surname', 'grade', 'school')

    def create(self, validated_data):
        validated_data['parent'] = self.context['request'].user
        return super().create(validated_data)

