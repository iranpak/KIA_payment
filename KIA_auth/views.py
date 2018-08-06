from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from KIA_auth.models import Profile
from django.contrib.auth import hashers

# Create your views here.


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        form_data = form.data
        print(form_data)
        if form.is_valid() and form_data['password1'] == form_data['password2']:
            cleaned_data = form.cleaned_data
            print(cleaned_data)
            username = cleaned_data.get('username')
            password = cleaned_data.get('password1')
            hashed_password = hashers.make_password(password)
            user = User.objects.create(username=username, password=hashed_password)
            user.first_name = cleaned_data.get('first_name')
            user.last_name = cleaned_data.get('last_name')
            user.email = cleaned_data.get('email')
            user.save()
            account_number = cleaned_data.get('account_number')
            phone_number = cleaned_data.get('phone_number')
            print(account_number, phone_number)
            profile = Profile.objects.create(user=user, phone_number=phone_number, account_number=account_number)
            profile.save()
            print(profile.phone_number)
            print(profile.account_number)
            print(user)
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse(str(form.errors))
    elif request.method == 'GET':
        form = SignUpForm()
        return render(request, 'KIA_auth/signup.html', {'form': form})
