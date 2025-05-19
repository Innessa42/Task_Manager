from django.db.models.functions import ExtractWeekDay
from rest_framework.exceptions import ValidationError
from django.db.models.aggregates import Count
from django.db.models import Count, QuerySet
from django.db.models.functions import ExtractWeekDay
from django.http import HttpResponse
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from task_manager_app.models import Task, SubTask, Category
from task_manager_app.serializers import TaskCreateSerializer, TaskListSerialize, TaskStatusCountSerializer, \
    SubTaskCreateSerializer, SubTaskSerializer, TaskDetailSerializer, CategoryCreateSerializer
from rest_framework import status, filters
from django.utils import timezone
from rest_framework.permissions import  SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend



def user_hallo(request):
    return HttpResponse("Hello, World")


class TaskListCreateView(ListCreateAPIView):
    WEEKDAY_MAP = {
        'воскресенье': 1,
        'sunday': 1,
        'понедельник': 2,
        'monday': 2,
        'вторник': 3,
        'tuesday': 3,
        'среда': 4,
        'wednesday': 4,
        'четверг': 5,
        'thursday': 5,
        'пятница': 6,
        'friday': 6,
        'суббота': 7,
        'saturday': 7,
    }

    queryset = Task.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskListSerialize
        return TaskCreateSerializer

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        day_of_week = self.request.query_params.get("weekday")

        if day_of_week:
            if day_of_week.lower() not in self.WEEKDAY_MAP:
                raise ValidationError("Неверный день недели!")

            weekday_num = self.WEEKDAY_MAP.get(day_of_week.lower())
            queryset = queryset.annotate(weekday=ExtractWeekDay('deadline')).filter(weekday=weekday_num)

        return queryset

class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    lookup_url_kwarg = 'task_id'
    permission_classes = [IsAuthenticatedOrReadOnly]


    def get_serializer_class(self):
            if self.request.method == 'GET':
                return TaskListSerialize
            return TaskCreateSerializer


#class TaskListCreateAPIView(APIView):
#     WEEKDAY_MAP = {
#         'воскресенье': 1,
#         'sunday': 1,
#         'понедельник': 2,
#         'monday': 2,
#         'вторник': 3,
#         'tuesday': 3,
#         'среда': 4,
#         'wednesday': 4,
#         'четверг': 5,
#         'thursday': 5,
#         'пятница': 6,
#         'friday': 6,
#         'суббота': 7,
#         'saturday': 7,
#     }
#
#     def get_queryset(self, request: Request) -> QuerySet[Task]:
#         queryset: QuerySet[Task] = Task.objects.all()
#         day_of_week = request.query_params.get("weekday")
#
#         if day_of_week:
#             if day_of_week not in self.WEEKDAY_MAP:
#                 raise ValidationError("Неверный день недели!")
#
#             weekday_num = self.WEEKDAY_MAP.get(day_of_week.lower())
#             queryset = queryset.annotate(weekday=ExtractWeekDay('deadline')).filter(weekday=weekday_num)
#
#         return queryset
#
#     def get(self, request: Request) -> Response:
#         tasks = self.get_queryset(request=request)
#         serializer = TaskListSerialize(tasks, many=True)
#
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_200_OK
#         )
#
#     def post(self, request: Request) -> Response:
#         serializer = TaskCreateSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#@api_view(['POST'])
#def tasks_create(request: Request) -> Response:
#    serializer = TaskCreateSerializer(data=request.data)
#
#    if serializer.is_valid():
#        serializer.save()
#        return Response(serializer.data, status=status.HTTP_201_CREATED)
#    else:
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#@api_view(['GET'])
#def list_of_tasks(request) -> Response:
#    tasks = Task.objects.all()
#    serializer = TaskListSerialize(tasks, many=True)
#
#    return Response(data=serializer.data, status=status.HTTP_200_OK)





#@api_view(['GET'])
#def get_task_by_id(request, task_id: int) -> Response:
#    try:
#        task = Task.objects.get(id=task_id)
#    except Task.DoesNotExist:
#        return Response(
#            data={
#                "message": "TASK NOT FOUND"
#            },
#            status=404
#        )

#    serializer = TaskListSerialize(task)
#
#    return Response(
#        data=serializer.data,
#        status=200
#    )
#
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



class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubTaskSerializer
        return SubTaskCreateSerializer

#class SubTaskListCreateAPIView(APIView, PageNumberPagination):
#     page_size = 2
#
#     def get_queryset(self, request: Request):
#
#         queryset: QuerySet[SubTask] = SubTask.objects.all()
#
#         tasks = request.query_params.getlist('task')
#         status = request.query_params.get('status')
#
#         if tasks:
#             queryset = queryset.filter(task__title__in=tasks)
#
#         if status:
#
#             valid_statuses = [choice[1] for choice in SubTask.STATUS_CHOICES]
#             if status in valid_statuses:
#
#                 queryset = queryset.filter(status=status)
#             else:
#
#                 queryset = queryset.none()
#
#         return queryset.order_by("-created_at")
#
#     def get_page_size(self, request):
#         page_size = request.query_params.get('page_size')
#
#         if page_size and page_size.isdigit():
#             return int(page_size)
#
#         return self.page_size
#
#     def get(self, request: Request) -> Response:
#         subtasks: QuerySet[SubTask] = self.get_queryset(request=request)
#         # subtasks: QuerySet[SubTask] = SubTask.objects.all().order_by("-created_at")
#         results = self.paginate_queryset(queryset=subtasks, request=request, view=self)
#         serializer = SubTaskSerializer(results, many=True)
#         # return Response(data=serializer.data, status=status.HTTP_200_OK)
#         return self.get_paginated_response(data=serializer.data)
#
#     def post(self, request: Request) -> Response:
#         serializer = SubTaskCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    lookup_url_kwarg = 'subtask_id'
    permission_classes = [IsAuthenticatedOrReadOnly]


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubTaskSerializer
        return SubTaskCreateSerializer


#class SubTaskDetailUpdateDeleteView(APIView):
#    def get(self, request: Request, **kwargs) -> Response:
#        try:
#            subtask = SubTask.objects.get(id=kwargs['subtask_id'])
#        except SubTask.DoesNotExist:
#            return Response(
#                data={
#                    "message": "Подзадача не найдена!"
#                },
#                status=status.HTTP_404_NOT_FOUND
#            )
#        serializer = SubTaskSerializer(subtask)
#
#        return Response(
#            data=serializer.data,
#            status=status.HTTP_200_OK
#        )
#
#    def put(self, request: Request, **kwargs) -> Response:
#        try:
#            subtask = SubTask.objects.get(id=kwargs['subtask_id'])
#        except SubTask.DoesNotExist:
#            return Response(
#                data={
#                    "message": "Подзадача не найдена!"
#                },
#                status=status.HTTP_404_NOT_FOUND
#            )
#
#        serializer = SubTaskCreateSerializer(instance=subtask, data=request.data)
#
#        if serializer.is_valid():
#            serializer.save()
#
#            return Response(
#                data=serializer.data,
#                status=status.HTTP_200_OK
#            )
#
#        else:
#            return Response(
#                data=serializer.errors,
#                status=status.HTTP_400_BAD_REQUEST
#            )
#
#    def delete(self, request: Request, **kwargs) -> Response:
#        try:
#            subtask = SubTask.objects.get(id=kwargs['subtask_id'])
#        except SubTask.DoesNotExist:
#            return Response(
#                data={
#                    "message": "Подзадача не найдена!"
#                },
#                status=status.HTTP_404_NOT_FOUND
#            )
#
#        subtask.delete()
#
#        return Response(
#            data={
#                "message": "Книга была успешно удалена."
#            },
#            status=status.HTTP_202_ACCEPTED
#        )
#
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAdminUser]

    @action(
        detail=False,
        methods=['get'],
        url_path='statistic'
    )
    def get_task_count_by_category(self, request: Request) -> Response:
        category_statistic = Category.objects.annotate(
            count_tasks=Count('task')
        )

        data = [
            {
                "id": c.id,
                "name": c.name,
                "count_tasks": c.count_tasks,
            }
            for c in category_statistic
        ]

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )



















