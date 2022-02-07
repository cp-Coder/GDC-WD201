from .models import Task, TaskChange
from django.dispatch import receiver
from django.db.models.signals import pre_save

@receiver(pre_save, sender=Task)
def generateHistory(instance, **kwargs):
  try:
    task = Task.objects.get(pk=instance.id)
  except:
    task = None
  
  if task is not None and task.status != instance.status:
    TaskChange.objects.create(task=task, previous_status=task.status, new_status=instance.status)
