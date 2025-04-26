from django.contrib import admin

# Register your models here.
from task_manager_app.models import Task, SubTask, Category

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1  # Количество пустых форм

#@admin.register(Task)
#class TaskAdmin(admin.ModelAdmin):
#    list_display = ('title', 'status', 'deadline', 'created_at')
#    list_filter = ('status', 'categories')
#    search_fields = ('title', 'description')
#
#@admin.register(SubTask)
#class SubTaskAdmin(admin.ModelAdmin):
#    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
#    list_filter = ('status')
#    search_fields = ('title', 'description')
#
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Админка для задач
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status',)
    inlines = [SubTaskInline]

    def short_title(self, obj):
        return obj.title[:10] + '...'
    short_title.short_description = 'Название'

# Админка для подзадач с action'ом
@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status',)
    actions = ['mark_done']

    @admin.action(description="Пометить выбранные как Done")
    def mark_done(self, request, queryset):
        updated = queryset.update(status='Done')
        self.message_user(request, f"Отмечено как Done: {updated}")
