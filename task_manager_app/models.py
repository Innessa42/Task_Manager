from django.contrib.auth.models import User
from django.db import models

from managers.category import SoftDeleteManager
from django.utils import timezone

#
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()

    def delete(self, *arg, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()

        self.save()


    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        unique_together = ("name",)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In_progress', 'In progress'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
        ('Done', 'Done'),
    ]


    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )



    title = models.CharField(max_length=100, unique_for_date='deadline')
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='New')
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

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    title = models.CharField(max_length=100)
    description = models.TextField()
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='New')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "task_manager_subtask"
        ordering = ('-created_at',)
        verbose_name = "SubTask"
        unique_together = ("title",)


    def __str__(self):
        return f"{self.title} ({self.task.title})"




