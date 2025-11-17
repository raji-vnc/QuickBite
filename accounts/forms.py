from django import forms
from accounts.models import User
from django.contrib.auth.forms import AuthenticationForm


class UserRegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','email','phone','address','password']

class LoginForm(AuthenticationForm):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
