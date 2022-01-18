from django import forms
from .models import Photograph, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class PhotoForm(forms.ModelForm):
    
    class Meta:
        model = Photograph
        fields = [ 'thumbnail', 'description']


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name']


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        ['username', 'first_name', 'last_name']
        exclude = ['user']
