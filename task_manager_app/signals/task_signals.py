from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from task_manager_app.models import Task

@receiver(pre_save, sender=Task)
def track_old_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Task.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Task.DoesNotExist:
            instance._old_status = None

#@receiver(post_save, sender=Task)
#def task_close_or_update_signal(sender, instance, created, **kwargs):
#    if not created:
#        if instance.status == 'Done':
#            send_mail(
#                subject=f'Задача - {instance.title} закрыта',
#                message=f'Задача - {instance.title} была закрыта пользователем {instance.owner.username}.',
#                from_email='no-reply.160924_ptm@gmail.com',
#                recipient_list=['admin.mail@gmail.com'],
#                fail_silently=False
#            )
#        elif hasattr(instance, '_old_status') and instance.status != instance._old_status:
#            send_mail(
#                subject=f'Статус задачи - {instance.title} был изменен',
#                message=f'Статус задачи - {instance.title} был изменен на {instance.status} пользователем {instance.owner.username}.',
#                from_email='no-reply.160924_ptm@gmail.com',
#                recipient_list=['admin.mail@gmail.com'],
#                fail_silently=False
#            )

@receiver(post_save, sender=Task)
def task_close_or_update_signal(sender, instance, created, **kwargs):
    if not created:
        if instance.status == 'Done':

                print(f'Задача - {instance.title} закрыта')
                print(f'Задача - {instance.title} была закрыта пользователем {instance.owner.username}.')


        elif hasattr(instance, '_old_status') and instance.status != instance._old_status:

                 print(f'Статус задачи - {instance.title} был изменен')
                 print(f'Статус задачи - {instance.title} был изменен на {instance.status} пользователем {instance.owner.username}.')

