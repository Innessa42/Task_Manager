from django.apps import AppConfig


class TaskManagerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_manager_app'

    def ready(self):
        import task_manager_app.signals.task_signals
















