import re

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
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
            "owner",
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
                  "owner",
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

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=[
            ("ADMIN", "ADMIN"),
            ("MODERATOR", "MODERATOR"),
            ("LIB MEMBER", "LIB MEMBER"),
        ],
        required=False
    )
    is_staff = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'first_name',
            'last_name', 'password',
            're_password', 'email',
            'role', 'is_staff',
        ]

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')

        re_pattern = r'^[a-zA-Z]+$'

        if not re.match(re_pattern, first_name):
            raise serializers.ValidationError(
                {"first_name": "First name must contain only alphabet characters."}
            )

        if not re.match(re_pattern, last_name):
            raise serializers.ValidationError(
                {"last_name": "Last name must contain only alphabet characters."}
            )

        password = attrs.get('password')
        re_password = attrs.pop('re_password', None)

        if not password:
            raise serializers.ValidationError(
                {"password": "This field is Required."}
            )

        if not re_password:
            raise serializers.ValidationError(
                {"re_password": "This field is Required."}
            )

        validate_password(password)

        if password != re_password:
            raise serializers.ValidationError(
                {"re_password": "Password didn't match."}
            )

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)

        user.save()

        return user













