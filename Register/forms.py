from django import forms
from django.contrib.auth.models import User
from .models import UserProfile,Post

class user_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','email','password')

class profile_form(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_URL','profile_pic')

class post_form(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['slug']
        widgets = {
            'author': forms.HiddenInput(),
        }