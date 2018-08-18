from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from KIA_auth.models import Profile
from django.contrib.auth import hashers
from django.core.mail import send_mail
# from django.contrib.auth.forms import S


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
            profile = Profile.objects.create(user=user, phone_number=phone_number, account_number=account_number)
            profile.save()
            send_registration_email(user.email)
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse(str(form.errors))
    elif request.method == 'GET':
        form = SignUpForm()
        return render(request, 'KIA_auth/signup.html', {'form': form})


def send_registration_email(email_address):
    subject = 'ثبت‌نام در سامانه KIA_payment'
    message_body = 'شما در سامانه KIA_payment ثبت‌نام کرده‌اید. برای فعالسازی حساب خود روی لینک زیر کلیک کنید.\n www.sample_link.com'
    sender_address = 'mh.iranpak1997@gmail.com'
    receiver_addresses = [email_address]
    send_mail(subject, message_body, sender_address, receiver_addresses)


def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = request.user
            user_profile = Profile.objects.get(user=user)

            information = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email,
                'account_number': user_profile.account_number,
                'phone_number': user_profile.phone_number,
            }

            form = SignUpForm()
            return render(request, 'KIA_auth/edit_profile.html', {'form': form, 'information': information})

        elif request.method == 'POST':
            form = SignUpForm(request.POST)
            form_data = form.data
            print(form_data)
            if form.is_valid() and form_data['password1'] == form_data['password2']:
                cleaned_data = form.cleaned_data
                print(cleaned_data)
                username = cleaned_data.get('username')
                password = cleaned_data.get('password1')
                hashed_password = hashers.make_password(password)
                user = User.objects.get(user=username)
                user.first_name = cleaned_data.get('first_name')
                user.last_name = cleaned_data.get('last_name')
                user.password = hashed_password
                user.email = cleaned_data.get('email')
                user.save()
                account_number = cleaned_data.get('account_number')
                phone_number = cleaned_data.get('phone_number')
                profile = Profile.objects.create(user=user, phone_number=phone_number, account_number=account_number)
                profile.save()
                return redirect('home')
            else:
                return HttpResponse(str(form.errors))
    else:
        return HttpResponse("no authenticate")
