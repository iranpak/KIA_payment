from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import SignUpForm
from .forms import EditProfileForm
from .forms import ChangePasswordForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from KIA_auth.models import Profile
from django.contrib.auth import hashers
from django.core.mail import send_mail
import requests
import json



access_denied_template = 'KIA_general/access_denied.html'
not_authorized_template = 'KIA_general/not_authorized.html'


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
            return render(request, 'KIA_auth/signup_error.html', {'errors': form.errors})
    elif request.method == 'GET':
        form = SignUpForm()
        return render(request, 'KIA_auth/signup.html', {'form': form})


def redirect_to_home(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if user_profile.is_restricted:
            return render(request, 'KIA_general/user_restricted.html')
        else:
            return render(request, 'KIA_auth/home.html')
    else:
        context = {}
        template = loader.get_template('KIA_general/not_authorized.html')
        return HttpResponse(template.render(context, request))


def send_registration_email(email_address):
    subject = 'ثبت‌نام در سامانه KIA_payment'
    message_body = 'شما در سامانه KIA_payment ثبت‌نام کرده‌اید. برای فعالسازی حساب خود روی لینک زیر کلیک کنید.\n www.sample_link.com'
    sender_address = 'kiapayment2018@gmail.com'
    receiver_addresses = [email_address]
    send_mail(subject, message_body, sender_address, receiver_addresses)


def edit_profile(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'GET':
            user_profile = Profile.objects.get(user=user)

            information = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email,
                'account_number': user_profile.account_number,
                'phone_number': user_profile.phone_number,
            }

            return render(request, 'KIA_auth/edit_profile.html', {'information': information})

        elif request.method == 'POST':
            form = EditProfileForm(request.POST)
            form_data = form.data
            print(form_data)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                print(cleaned_data)
                user = User.objects.get(username=user.username)

                user.first_name = cleaned_data.get('first_name')
                user.last_name = cleaned_data.get('last_name')
                user.save()

                account_number = cleaned_data.get('account_number')
                phone_number = cleaned_data.get('phone_number')
                user_profile = Profile.objects.get(user=user)
                user_profile.phone_number = phone_number
                user_profile.account_number = account_number
                user_profile.save()
                return redirect('edit_profile')
            else:
                return HttpResponse(str(form.errors))
    else:
        return render(request, not_authorized_template)


def change_password(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'KIA_auth/change_password.html')

        elif request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            form_data = form.data
            print(form_data)
            if form.is_valid():
                if form_data['new_password'] == form_data['new_password_confirmation']:
                    user = User.objects.get(username=user.username)
                    cleaned_data = form.cleaned_data
                    print(cleaned_data)
                    old_password = cleaned_data.get('old_password')
                    new_password = cleaned_data.get('new_password')
                    new_hashed_password = hashers.make_password(new_password)
                    if user.check_password(old_password):
                        user.password = new_hashed_password
                        user.save()
                        login(request, user)
                        return redirect('home')
                    else:
                        return HttpResponse("Old password is wrong")
                else:
                    return HttpResponse("Passwords doesn't match")
            else:
                print(str(form.errors))
                return HttpResponse(str(form.errors))
    else:
        return render(request, not_authorized_template)


def add_credit(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if request.method == 'GET':
            current_credit = user_profile.credit
            return render(request, 'KIA_auth/add_credit.html', {'current_credit': current_credit})

        elif request.method == 'POST':
                increasing_credit = int(request.POST.get("added_credit"))
                user_profile.credit += increasing_credit
                user_profile.save()
                return redirect('home')
    else:
        return render(request, not_authorized_template)


def withdraw_credit(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if request.method == 'GET':
            current_credit = user_profile.credit
            return render(request, 'KIA_auth/withdraw_credit.html', {'current_credit': current_credit})

        elif request.method == 'POST':
            withdrawing_credit = int(request.POST.get("sub_credit"))
            user_profile.credit -= withdrawing_credit
            user_profile.save()
            current_credit = user_profile.credit
            return render(request, 'KIA_auth/withdraw_credit.html', {'current_credit': current_credit})
    else:
        return render(request, not_authorized_template)


def anonymous_transfer(request):
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
            return render(request, 'KIA_auth/anonymous_transfer.html', {'form': form, 'information': information})

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
        context = {}
        template = loader.get_template('KIA_general/not_authorized.html')
        return HttpResponse(template.render(context, request))
        # return HttpResponse("not authorized")


def transaction_history(request):
    acts = [
        {'type': 'TOEFL',
         'amount': '10000',
         'date': '29.9.2018'},
        {'type': 'University',
         'amount': '4624',
         'date': '29.9.2018'},
        {'type': 'TOEFL',
         'amount': '435',
         'date': '29.9.2018'},
        {'type': 'TOEFL',
         'amount': '234646',
         'date': '29.9.2018'},
        {'type': 'GRE',
         'amount': '13423',
         'date': '29.9.2018'},
    ]
    return render(request, 'KIA_auth/transaction_history.html', {'acts': acts})






















