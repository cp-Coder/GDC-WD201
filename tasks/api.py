from django.db import transaction
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .filter import TaskChangeFilter, TaskFilter
from .models import Task, TaskChange
from .serializers import TaskSerializer, TaskChangeSerializer
from django_filters.rest_framework import DjangoFilterBackend

class TaskViewSet(ModelViewSet):
  permission_classes = [IsAuthenticated]
  queryset = Task.objects.all()
  serializer_class = TaskSerializer
  filterset_class = TaskFilter
  filter_backends = [DjangoFilterBackend]

  def get_queryset(self):
    return Task.objects.filter(user=self.request.user, deleted=False)
  
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  @transaction.atomic
  def create(self, request, *args, **kwargs):
    return super().create(request, *args, **kwargs)
  
  @transaction.atomic
  def update(self, request, *args, **kwargs):
    return super().update(request, *args, **kwargs)

class TaskChangeViewSet(mixins.ListModelMixin, GenericViewSet):
  permission_classes = [IsAuthenticated]
  queryset = TaskChange.objects.all()
  serializer_class = TaskChangeSerializer
  filterset_class = TaskChangeFilter
  filter_backends = [DjangoFilterBackend]

  def get_queryset(self):
    if "task_pk" in self.kwargs:
      return TaskChange.objects.filter(task=self.kwargs["task_pk"], task__user=self.request.user)
    return TaskChange.objects.filter(task__user=self.request.user)