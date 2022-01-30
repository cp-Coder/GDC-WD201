from django.urls import path

from tasks.views import (
    TaskCreateView,
    TaskDeleteView,
    TaskListView,
    TaskUpdateView,
)

urlpatterns = [
    path("", TaskListView.as_view(), name="tasks-list"),
    path("add/", TaskCreateView.as_view(), name="tasks-add"),
    path("update/<int:pk>/", TaskUpdateView.as_view(), name="tasks-update"),
    path("delete/<int:pk>/", TaskDeleteView.as_view(), name="tasks-delete"),
]
