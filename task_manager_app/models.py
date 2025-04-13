from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        unique_together = ("name",)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=100, unique_for_date='deadline')
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "task_manager_task"
        ordering = ('-created_at',)
        verbose_name = "Task"
        unique_together = ("title",)

    def __str__(self):
        return self.title

class SubTask(models.Model):
    STATUS_CHOICES = Task.STATUS_CHOICES


    title = models.CharField(max_length=100)
    description = models.TextField()
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "task_manager_subtask"
        ordering = ('-created_at',)
        verbose_name = "SubTask"
        unique_together = ("title",)

    def __str__(self):
        return f"{self.title} ({self.task.title})"