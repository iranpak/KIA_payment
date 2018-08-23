from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from KIA_auth.models import Profile
from .models import SystemCredit
from .models import HistoryOfAdminActivities
from .models import SystemTransactions
from django.template import loader
from django.contrib.auth import hashers
from django.core.mail import send_mail
from KIA_auth.forms import AdminCreateUserForm
from django.shortcuts import redirect


access_denied_template = 'KIA_general/access_denied.html'
not_authorized_template = 'KIA_general/not_authorized.html'


def restrict_user(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if user_profile.role == 'Admin':
            # TODO: show field for restricting user
            user_profile.is_restricted = True
            user_profile.save()
            context = {}
            template = loader.get_template('KIA_admin/restrict_user.html')
            return HttpResponse(template.render(context, request))
            # return HttpResponse("user restricted")

        else:
            return render(request, access_denied_template)
    else:
        return render(request, not_authorized_template)


def remove_user_restriction(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if user_profile.role == 'Admin':
            # TODO: show field for restricting user
            user_profile.is_restricted = False
            user_profile.save()
            context = {}
            template = loader.get_template('KIA_admin/remove_restriction.html')
            return HttpResponse(template.render(context, request))
        else:
            return render(request, access_denied_template)
    else:
        return render(request, not_authorized_template)


def panel(request):
    context = {}
    template = loader.get_template('KIA_admin/admin_panel.html')
    return HttpResponse(template.render(context, request))


def users_activities(request):
    acts = [
        {'username': 'hello',
         'type': 'purchase',
         'date': '29.9.2018'},
        {'username': 'hi',
         'type': 'charge',
         'date': '10.11.2010'},
        {'username': 'lol',
         'type': 'steal',
         'date': '25.2.2018'},
        {'username': 'user',
         'type': 'charge',
         'date': '5.3.2018'},
    ]
    return render(request, 'KIA_admin/users_activities.html', {'acts': acts})


def employees_activities(request):
    context = {}
    template = loader.get_template('KIA_admin/employees_activities.html')
    return HttpResponse(template.render(context, request))


def my_history(request):
    template = 'KIA_admin/my_history.html'
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if user_profile.role == 'Admin':
            actions = HistoryOfAdminActivities.objects.all()
            return render(request, template, {'actions': actions})
        else:
            return render(request, access_denied_template)
    else:
        return render(request, not_authorized_template)


def financial_account_details(request):
    context = {}
    template = loader.get_template('KIA_admin/financial_account_details.html')
    return HttpResponse(template.render(context, request))


def add_system_credit(request):
    user = request.user
    template = 'KIA_admin/add_system_credit.html'

    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if user_profile.role == 'Admin':
            if request.method == 'GET':
                # TODO: show field for restricting user
                return render(request, template)
            elif request.method == 'POST':
                increasing_credit = request.POST.get("added_credit")
                system_credit = SystemCredit.objects.get(owner='system')
                system_credit.rial_credit += increasing_credit
                system_credit.save()
        else:
            return render(request, access_denied_template)
    else:
        return render(request, not_authorized_template)


def add_transaction(request):
    context = {}
    template = loader.get_template('KIA_admin/add_transaction.html')
    return HttpResponse(template.render(context, request))


def add_user(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if user_profile.role == 'Admin':
            if request.method == 'GET':
                form = AdminCreateUserForm()
                return render(request, 'KIA_admin/add_user.html', {'form': form})
            elif request.method == 'POST':
                if request.method == 'POST':
                    form = AdminCreateUserForm(request.POST)
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
                        role = cleaned_data.get('role')
                        profile = Profile.objects.create(user=user, phone_number=phone_number,
                                                         account_number=account_number, role=role)
                        profile.save()
                        send_registration_email(user.email, username, password, role)
                        return redirect('admin_panel')
        else:
            return render(request, access_denied_template)
    else:
        return render(request, not_authorized_template)


def send_registration_email(email_address, username, password, role):
    subject = 'ثبت‌نام در سامانه KIA_payment'
    message_body = ('برای شما در سامانه KIA_payment یک حساب کاربری ساخته شده است. برای فعالسازی حساب خود روی لینک زیر کلیک کنید.\n www.sample_link.com\n نقش شما: %s \n نام کاربری: %s \n رمز عبور: %s \n' %(role, username, password))
    sender_address = 'kiapayment2018@gmail.com'
    receiver_addresses = [email_address]
    send_mail(subject, message_body, sender_address, receiver_addresses)


def show_system_transactions(request):
    template = 'KIA_admin/show_system_transactions.html'
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if user_profile.role == 'Admin':
            transactions = SystemTransactions.objects.all()
            return render(request, template, {'transactions': transactions})
        else:
            return render(request, access_denied_template)
    else:
        return render(request, not_authorized_template)
