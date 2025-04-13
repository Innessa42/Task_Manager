from django.contrib import admin

# Register your models here.
from .models import Task, SubTask, Category

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'categories')
    search_fields = ('title', 'description')

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'description')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)