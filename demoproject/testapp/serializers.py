from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.Serializer):
    title=serializers.CharField(max_length=100)
    discription=serializers.CharField(max_length=100)
    completed=serializers.BooleanField(default=False)

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title=validated_data.get('title', instance.title)
        instance.discription=validated_data.get('discription', instance.discription) 
        instance.completed=validated_data.get('completed', instance.completed)
        instance.save()
        return instance   