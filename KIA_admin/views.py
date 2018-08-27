from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from KIA_auth.models import Profile
from .models import SystemCredit
from .models import HistoryOfAdminActivities
from .models import SystemTransactions
from django.contrib.auth import hashers
from django.core.mail import send_mail
from KIA_auth.forms import AdminCreateUserForm
from django.shortcuts import redirect
from KIA_services.models import KIAService, KIATransaction, KIAServiceField

access_denied_template = 'KIA_general/access_denied.html'
not_authorized_template = 'KIA_general/not_authorized.html'


def is_user_admin(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        role = user_profile.role
        if role == 'Admin':
            return True
        return False
    return False


def is_user_emp(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        role = user_profile.role
        if role == 'Employee':
            return True
        return False
    return False


def restrict_user(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if is_user_admin(request):
            if request.method == 'GET':
                return render(request, 'KIA_admin/restrict_user.html')
            elif request.method == 'POST':
                restricting_username = request.POST.get("res_username")
                if restricting_username:
                    restricting_message = request.POST.get("restrict_message")
                    try:
                        restricting_user = User.objects.get(username=restricting_username)
                        restricting_user_profile = Profile.objects.get(user=restricting_user)
                        restricting_user_profile.is_restricted = True
                        restricting_user_profile.save()
                        description = 'شما دسترسی کاربر %s را مسدود کردید.' % restricting_user
                        HistoryOfAdminActivities.objects.create(type='User restriction', description=description,
                                                                message=restricting_message)

                        return render(request, 'KIA_general/success.html',
                                      {'message': 'کاربر با موفقیت مسدود شد', 'return_url': 'restrict_user'})

                    except Exception as e:
                        print(e)
                        errors = {'username': 'There is no user with this username'}
                        return render(request, 'KIA_admin/restrict_user.html', {'errors': errors})
                else:
                    return redirect('restrict_user')
        else:
            return render(request, access_denied_template)
    else:
        return render(request, not_authorized_template)


def remove_user_restriction(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if is_user_admin(request):
            if request.method == 'GET':
                return render(request, 'KIA_admin/remove_restriction.html')
            elif request.method == 'POST':
                restricting_username = request.POST.get("res_username")
                restricting_message = request.POST.get("restrict_message")
                if restricting_username:
                    try:
                        restricting_user = User.objects.get(username=restricting_username)
                        restricting_user_profile = Profile.objects.get(user=restricting_user)
                        restricting_user_profile.is_restricted = False
                        restricting_user_profile.save()
                        description = 'شما دسترسی کاربر %s را باز کردید.' % restricting_user
                        HistoryOfAdminActivities.objects.create(type='User restriction',
                                                                description=description, message=restricting_message)
                        # return redirect('remove_user_restriction')
                        return render(request, 'KIA_general/success.html',
                                      {'message': 'دسترسی کاربر با موفقیت باز شد', 'return_url': 'remove_user_restriction'})

                    except Exception as e:
                        errors = {'username': 'There is no user with this username'}
                        return render(request, 'KIA_admin/remove_restriction.html', {'errors': errors})
                else:
                    return redirect('remove_user_restriction')

        else:
            return render(request, access_denied_template)
    else:
        return render(request, not_authorized_template)


def panel(request):
    if not request.user.is_authenticated:
        return render(request, not_authorized_template)
    if not is_user_admin(request):
        return render(request, access_denied_template)

    user = request.user
    user_profile = Profile.objects.get(user=user)

    return render(request, 'KIA_admin/admin_panel.html', {'email': user_profile.user.email,
                                                          'name': user_profile.user.first_name,
                                                          'username': user_profile.user.username})


def activities(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if is_user_admin(request):
            registered_transactions = KIATransaction.objects.filter(state=KIATransaction.registered)
            being_done_transactions = KIATransaction.objects.filter(state=KIATransaction.being_done)
            suspicious_transactions = KIATransaction.objects.filter(state=KIATransaction.suspicious)
            finished_transactions = KIATransaction.objects.filter(state=KIATransaction.done)
            failed_transactions = KIATransaction.objects.filter(state=KIATransaction.failed)

            return render(request, 'KIA_admin/activities.html'
                          , {'registered': registered_transactions,
                             'suspicious': suspicious_transactions,
                             'being_done': being_done_transactions,
                             'done': finished_transactions,
                             'failed': failed_transactions, })
            # return render(request, 'KIA_admin/activities.html')  # TODO panel info
        else:
            return render(request, access_denied_template)
    else:
        return render(request, not_authorized_template)


def my_history(request):
    template = 'KIA_admin/my_history.html'
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if is_user_admin(request):
            actions = HistoryOfAdminActivities.objects.all()
            return render(request, template, {'actions': actions})
        else:
            return render(request, access_denied_template)
    else:
        return render(request, not_authorized_template)


def financial_account_details(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if is_user_admin(request):
            return render(request, 'KIA_admin/financial_account_details.html')  # TODO panel info
        else:
            return render(request, access_denied_template)
    else:
        return render(request, not_authorized_template)


def add_system_credit(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        system_credit = SystemCredit.objects.get(owner='system')
        if is_user_admin(request):
            if request.method == 'GET':
                current_rial_credit = system_credit.rial_credit
                current_dollar_credit = system_credit.dollar_credit
                return render(request, 'KIA_admin/add_system_credit.html', {'current_rial_credit': current_rial_credit,
                                                                            'current_dollar_credit': current_dollar_credit})
            elif request.method == 'POST':
                increasing_credit = int(request.POST.get("added_credit"))
                selected_credit = request.POST.get("selected_credit")
                description = "افزایش اعتبار سامانه"
                if selected_credit == 'rial_credit':
                    system_credit.rial_credit += increasing_credit
                    description = 'افزایش اعتبار ریالی سامانه به میزان %s ریال' % increasing_credit
                elif selected_credit == 'dollar_credit':
                    system_credit.dollar_credit += increasing_credit
                    description = 'افزایش اعتبار ارزی سامانه به میزان %s دلار' % increasing_credit

                system_credit.save()
                HistoryOfAdminActivities.objects.create(type='Charge', description=description)
                return redirect('add_system_credit')
        else:
            return render(request, access_denied_template)
    else:
        return render(request, not_authorized_template)


def add_user(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if is_user_admin(request):
            if request.method == 'GET':
                form = AdminCreateUserForm()
                return render(request, 'KIA_admin/add_user.html', {'form': form})
            elif request.method == 'POST':
                form = AdminCreateUserForm(request.POST)
                form_data = form.data
                print(form_data)
                if form.is_valid() and form_data['password1'] == form_data['password2']:
                    cleaned_data = form.cleaned_data

                    # all_users = User.objects.all()
                    # for user in all_users:
                    #     if user.email == cleaned_data.get('email'):
                    #         errors = {'email': 'A user already exists with this email'}
                    #         return render(request, 'KIA_admin/add_user.html', {'errors': errors, 'form': form})

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
                    role = request.POST.get("role")
                    print(role)
                    profile = Profile.objects.create(user=user, phone_number=phone_number,
                                                     account_number=account_number, role=role)
                    profile.save()
                    description = 'ایجاد کاربر با نام  کاربری %s' % username
                    HistoryOfAdminActivities.objects.create(type='Create user', description=description)
                    send_registration_email(user.email, username, password, role)
                    return redirect('admin_panel')
                else:
                    return render(request, 'KIA_admin/add_user.html', {'form': form})
        else:
            return render(request, access_denied_template)
    else:
        return render(request, not_authorized_template)


def send_registration_email(email_address, username, password, role):
    subject = 'ثبت‌نام در سامانه KIA_payment'
    message_body = 'برای شما در سامانه کیاپرداخت یک حساب کاربری به عنوان %s ساخته شده است.' % role
    message_body += '\n'
    message_body += 'username: %s \n' % username
    message_body += 'password: %s \n' % password
    sender_address = 'kiapayment2018@gmail.com'
    receiver_addresses = [email_address]
    send_mail(subject, message_body, sender_address, receiver_addresses)


def show_system_transactions(request):
    template = 'KIA_admin/show_system_transactions.html'
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if is_user_admin(request):
            transactions = SystemTransactions.objects.all()
            return render(request, template, {'transactions': transactions})
        else:
            return render(request, access_denied_template)
    else:
        return render(request, not_authorized_template)
