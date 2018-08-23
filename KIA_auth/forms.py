from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    account_number = forms.CharField()
    phone_number = forms.CharField(max_length=11)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email', 'account_number',
                  'phone_number')


class AdminCreateUserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    role = forms.CharField()
    email = forms.EmailField()
    account_number = forms.CharField()
    phone_number = forms.CharField(max_length=11)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email', 'account_number',
                  'phone_number', 'role')

