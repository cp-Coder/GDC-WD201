from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

STATUS_CHOICES = (
 ("PENDING", "PENDING"),
 ("IN_PROGRESS", "IN_PROGRESS"),
 ("COMPLETED", "COMPLETED"),
 ("CANCELLED", "CANCELLED"),
)
class Task(models.Model):
  title = models.CharField(max_length=100, blank=True)
  description = models.TextField(blank=True)
  priority = models.IntegerField(default=0)
  completed = models.BooleanField(default=False)
  created_date = models.DateTimeField(auto_now=True)
  deleted = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

class TaskChange(models.Model):
  task = models.ForeignKey(Task, on_delete=models.CASCADE)
  previous_status = models.CharField(max_length=100, choices=STATUS_CHOICES)
  new_status = models.CharField(max_length=100, choices=STATUS_CHOICES)
  changed_date = models.DateTimeField(auto_now=True)


class Report(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  time = models.TimeField(null=True)
  last_updated = models.DateTimeField(null=True)
  send_report = models.BooleanField(default=True)

  def save(self, *args, **kwargs):
    if not self.last_updated:
      self.last_updated = now()
    super().save(*args, **kwargs)