from rest_framework import serializers

from task_manager_app.models import Task, SubTask, Category
from django.utils import timezone

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


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        read_only=True
    )

    class Meta:
        model = SubTask
        fields = ["title",
                  "description",
                  "task",
                  "status",
                  "deadline",
                  "created_at"]

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]

    def validate_name(self, value: str):
        if value:
            unique_name = Category.objects.filter(name__iexact=value).exists()
            if unique_name:
                raise serializers.ValidationError(
                    "Така категория уже существует!"
                )
        return value

class SubTaskSerializer(serializers.ModelSerializer):
    task = serializers.StringRelatedField()

    class Meta:
        model = SubTask
        fields = "__all__"


class TaskDetailSerializer(serializers.ModelSerializer):
    subtask_set = SubTaskSerializer(many=True)

    class Meta:
        model = Task
        fields = "__all__"


class TaskCreateSerialize(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "categories",
            "deadline"
        ]

    def validate_deadline(self, value: str):
        if value < timezone.now():
            raise serializers.ValidationError(
                f"Дата не может быть меньше {timezone.now()}"
            )
        return value














