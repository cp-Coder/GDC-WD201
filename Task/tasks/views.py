from django import forms
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from .mixins import OwnerMixin
from .models import Task, Report, STATUS_CHOICES
from django.db import transaction


class TaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = ["title", "description", "priority", "status", "completed"]
    widgets = {
        "title": forms.TextInput(attrs={"class": "form-control"}),
        "description": forms.Textarea(attrs={"class": "form-control"}),
        "priority": forms.NumberInput(attrs={"class": "form-control"}),
        "status": forms.Select(attrs={"class": "form-selected border border-gray-300 rounded-md ml-5 text-gray-600 h-10 pl-5 px-2 pr-10 bg-white hover:border-gray-400 focus:outline-none appearance-none "}, choices=STATUS_CHOICES),
        "completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
      }

class UserSettingsForm(forms.ModelForm):  

    class Meta:
        model = Report
        fields = ("time", "send_report")
        widgets = {
            "time": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "send_report": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
class BaseTaskView(OwnerMixin):
  model = Task
  form_class = TaskForm
  queryset = Task.objects.filter(deleted=False).order_by("priority")
  context_object_name = "tasks"
  success_url = "/tasks/"

  def form_valid(self, form):
    if self.request.POST.get("confirm_delete"):
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    if form.instance.completed:
        # task is completed
        self.object = form.save()
        self.object.completed = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    # current task priority
    current_priority = form.instance.priority
    # get all the tasks having greater priority using __gte
    # and then update the conflicting priorities
    tasks = (
        Task.objects.filter(
            user=self.request.user,
            priority__gte=current_priority,
            deleted=False,
            completed=False,
        )
        .exclude(pk=form.instance.id)
        .select_for_update()
        .order_by("priority")
    )
    # use transaction.atomic() to commit all the queries in one go as well as
    # rollback to previous savepoint in case of exception

    with transaction.atomic():
        temp = []
        for task in tasks:
            if task.priority > current_priority:
                break
            current_priority += 1
            task.priority = current_priority
            temp.append(task)
        if temp:
            Task.objects.bulk_update(temp, ["priority"], batch_size=500)
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
    return HttpResponseRedirect(self.get_success_url())


class TaskListView(BaseTaskView, ListView):
  template_name = "tasks/tasks.html"
  paginate_by = 5

  def get_context_data(self, **kwargs):
    context_data = super().get_context_data(**kwargs)
    context_data["completed_tasks"] = self.queryset.filter(
        completed=True, user=self.request.user
    ).count()
    context_data["total_tasks"] = self.queryset.filter(
        user=self.request.user
    ).count()
    return context_data

  def get_queryset(self):
    queryset = super().get_queryset()
    status = self.request.GET.get("status")
    if status == "completed":
        queryset = queryset.filter(completed=True)
    elif status == "pending":
        queryset = queryset.filter(completed=False)
    return queryset


class TaskCreateView(BaseTaskView, CreateView):
  ...


class TaskUpdateView(BaseTaskView, UpdateView):
  ...


class TaskDeleteView(BaseTaskView, DeleteView):
  form_class = forms.Form

class UserSettingsView(OwnerMixin, UpdateView):
    form_class = UserSettingsForm
    template_name = "tasks/user_settings.html"
    success_url = "/tasks/"

    def get_object(self):
        return Report.objects.get_or_create(user=self.request.user)[0]