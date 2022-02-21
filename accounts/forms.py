from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
  password2 = forms.CharField(label='password', widget=forms.PasswordInput)
  class Meta:
    model = User
    fields = ['username']
    
  def username_clean(self):  
    username = self.cleaned_data['username'].lower()  
    new = User.objects.filter(username = username)  
    if new.count():  
      raise ValidationError("User Already Exist")  
    return username   
    
  def clean_password2(self):  
    password1 = self.cleaned_data['password1']  
    password2 = self.cleaned_data['password2']  
    if password1 and password2 and password1 != password2:  
      raise ValidationError("Password don't match")  
    return password1  
    
  def save(self, commit = True):  
    user = super(SignUpForm, self).save(commit=False)
    if commit:
      user.save()
    return user  
