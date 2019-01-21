from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
    attrs = {
        'placeholder' : 'Password',
        'class':'form-control',
        'required':'required'
    }
    ))
    username = forms.CharField(widget=forms.TextInput(
    attrs = {
        'placeholder' : 'Username',
        'class':'form-control',
        'required':'required'
    }
    ))
    email = forms.CharField(widget=forms.TextInput(
    attrs = {
        'placeholder' : 'Email',
        'class':'form-control',
        'type':'email',
        'required':'required'
    }
    ))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
