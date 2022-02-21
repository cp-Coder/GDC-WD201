from django.urls import path
from tasks.views import TaskListView, TaskCreateView, TaskDeleteView, TaskUpdateView, UserSettingsView

urlpatterns = [
    path("", TaskListView.as_view(), name="tasks-list"),
    path("add/", TaskCreateView.as_view(), name="tasks-add"),
    path("update/<int:pk>/", TaskUpdateView.as_view(), name="tasks-update"),
    path("delete/<int:pk>/", TaskDeleteView.as_view(), name="tasks-delete"),
    path("user/report/", UserSettingsView.as_view(), name="user-settings"),
] 
