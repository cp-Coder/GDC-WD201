from django.contrib import admin
from tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "priority", "deleted", "user")


admin.sites.site.register(Task, TaskAdmin)
