from rest_framework.serializers import ModelSerializer
from .models import Task, TaskChange


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "priority",
            "status",
            "user",
            "created_date",
        )
        read_only_fields = ("user", "created_date")


class TaskChangeSerializer(ModelSerializer):
    class Meta:
        model = TaskChange
        fields = ("id", "task", "previous_status", "new_status", "changed_date")
