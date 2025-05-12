from rest_framework import serializers

from task_manager_app.models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'deadline',
            'categories',
        ]


class TaskListSerialize(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskStatusCountSerializer(serializers.Serializer):
    status = serializers.CharField()
    id__count = serializers.IntegerField()
