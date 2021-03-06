import imp
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import UserLoginView, UserSignUpView

urlpatterns = [
  path("login/", UserLoginView.as_view(), name="login"), 
  path("signup/", UserSignUpView.as_view(), name="signup"),
  path("logout/", LogoutView.as_view(), name="logout"),
]
