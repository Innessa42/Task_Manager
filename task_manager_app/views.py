from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import  Request

from task_manager_app.models import Task
from task_manager_app.serializers import TaskCreateSerializer, TaskListSerialize, TaskStatusCountSerializer
from rest_framework import status
from django.utils import timezone

def user_hallo(request):
    return HttpResponse("Hello, World")

@api_view(['POST'])
def tasks_create(request: Request) -> Response:
    serializer = TaskCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_of_tasks(request) -> Response:
    tasks = Task.objects.all()
    serializer = TaskListSerialize(tasks, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_task_by_id(request, task_id: int) -> Response:
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response(
            data={
                "message": "TASK NOT FOUND"
            },
            status=404
        )

    serializer = TaskListSerialize(task)

    return Response(
        data=serializer.data,
        status=200
    )

@api_view(['GET'])
def tasks_count(request) -> Response:
    tasks_cn = Task.objects.count()

    return Response(data=f"{tasks_cn=}", status=status.HTTP_200_OK)

@api_view(['GET'])
def tasks_count_by_status(request) -> Response:
    statuses_count_by_task = Task.objects.values("status").annotate(Count("id"))
    serializer = TaskStatusCountSerializer(statuses_count_by_task, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def tasks_of_overdue(request) -> Response:
    count_of_overdue_task = Task.objects.filter(deadline__lt=timezone.now()).count()

    return Response(data=f"{count_of_overdue_task=}", status=status.HTTP_200_OK)
