"""
URL configuration for task_manager_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from task_manager_app.views import user_hallo, tasks_count, \
    tasks_count_by_status, tasks_of_overdue, SubTaskDetailUpdateDeleteView, \
    TaskListCreateView, TaskDetailUpdateDeleteView, SubTaskListCreateView, CategoryViewSet, UserTasksListGenericView, \
    UserSubTasksListGenericView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Task API',
        default_version='v1',
        description='Our Task API with permissions',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(name='innag', email='net@net.net'),
        license=openapi.License(name='OUR LICENSE', url='https://example.com')
    ),
    public=False,
    permission_classes=[permissions.IsAdminUser],
)


router = DefaultRouter()
router.register('categories', CategoryViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("hallo/", user_hallo),
    #path("task/create/", tasks_create),
    path("tasks/", TaskListCreateView.as_view()),
    path('tasks/<int:task_id>', TaskDetailUpdateDeleteView.as_view()),
    path('tasks-me/', UserTasksListGenericView.as_view()),
    path('tasks/count', tasks_count),
    path('tasks/status_count', tasks_count_by_status),
    path('tasks/tasks_of_overdue', tasks_of_overdue),
    path('subtasks/', SubTaskListCreateView.as_view()),
    path('subtasks/<int:subtask_id>', SubTaskDetailUpdateDeleteView.as_view()),
    path('subtasks-me/', UserSubTasksListGenericView.as_view()),
    path('', include(router.urls)),
    path('auth-login-jwt/', TokenObtainPairView.as_view()),
    path('token_refresh/', TokenRefreshView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]
