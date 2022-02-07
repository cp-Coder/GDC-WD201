from django_filters.rest_framework import CharFilter, ChoiceFilter, FilterSet
from .models import STATUS_CHOICES, Task, TaskChange

class TaskFilter(FilterSet):
  title = CharFilter(lookup_expr="icontains")
  status = ChoiceFilter(choices=STATUS_CHOICES)

  class Meta:
    model = Task
    fields = ("title", "status")


class TaskChangeFilter(FilterSet):
  previous_status = ChoiceFilter(choices=STATUS_CHOICES)
  new_status = ChoiceFilter(choices=STATUS_CHOICES)

  class Meta:
    model = TaskChange
    fields = ("previous_status", "new_status", "changed_date")