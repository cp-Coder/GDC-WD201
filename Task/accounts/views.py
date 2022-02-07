from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from .forms import SignUpForm

class UserSignUpView(CreateView):
  form_class = SignUpForm
  template_name = "accounts/signup.html"
  success_url = "/user/login/"
  
class UserLoginView(LoginView):
  template_name = "accounts/login.html"

