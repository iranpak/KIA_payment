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


class EditProfileForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    account_number = forms.CharField(required=True)
    phone_number = forms.CharField(max_length=11)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(required=True)
    new_password = forms.CharField(required=True)
    new_password_confirmation = forms.CharField(required=True)


# class AnonymousTransferForm(forms.Form):
