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
from django.urls import path
from task_manager_app.views import user_hallo, tasks_create, list_of_tasks, get_task_by_id, tasks_count, \
    tasks_count_by_status, tasks_of_overdue, SubTaskListCreateAPIView, SubTaskDetailUpdateDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("hallo/", user_hallo),
    path("task/create/", tasks_create),
    path("tasks/", list_of_tasks),
    path('tasks/<int:task_id>', get_task_by_id),
    path('tasks/count', tasks_count),
    path('tasks/status_count', tasks_count_by_status),
    path('tasks/tasks_of_overdue', tasks_of_overdue),
    path('subtasks/', SubTaskListCreateAPIView.as_view()),
    path('subtasks/<int:subtask_id>', SubTaskDetailUpdateDeleteView.as_view()),

]
