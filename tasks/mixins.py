from multiprocessing.spawn import import_main_path
from re import I
from django.contrib.auth.mixins import LoginRequiredMixin

class OwnerMixin(LoginRequiredMixin):
  def get_queryset(self):
    queryset = super().get_queryset()
    return queryset.filter(user=self.request.user)