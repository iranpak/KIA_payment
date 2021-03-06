from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from KIA_services.models import KIATransaction
from .forms import SignUpForm
from .forms import EditProfileForm
from .forms import ChangePasswordForm
from .forms import AnonymousTransferForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from KIA_auth.models import Profile
from django.contrib.auth import hashers
from django.core.mail import send_mail
from django.db.models import Sum, Count

import string, random

access_denied_template = 'KIA_general/access_denied.html'
not_authorized_template = 'KIA_general/not_authorized.html'


def sign_up(request):
    if request.method == 'GET':
        form = SignUpForm()
        if request.user.is_authenticated:
            return redirect_to_home(request)
        return render(request, 'KIA_auth/signup.html',
                      {'form': form})

    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        form_data = form.data
        if form.is_valid():
            cleaned_data = form.cleaned_data

            # all_users = User.objects.all()
            # for user in all_users:
            #     if user.email == cleaned_data.get('email'):
            #         errors = {'email': 'A user already exists with this email'}
            #         return render(request, 'KIA_auth/signup.html', {'errors': errors, 'form': form})

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
            return render(request, 'KIA_auth/signup.html',
                          {'form': form, 'role': Profile.objects.get(user=request.user).role, })


def redirect_to_home(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if user_profile.is_restricted:
            return render(request, 'KIA_general/user_restricted.html',
                          {'role': Profile.objects.get(user=request.user).role, })
        else:
            if user_profile.role == 'Admin':
                total_rial = \
                    KIATransaction.objects.filter(state=KIATransaction.done).aggregate(total=Sum('cost_in_rial'))[
                        'total']
                done = KIATransaction.objects.filter(state=KIATransaction.done).count()
                fail = KIATransaction.objects.filter(state=KIATransaction.failed).count()

                return render(request, 'KIA_admin/admin_panel.html',
                              {'total_rial': total_rial,
                               'done': done,
                               'fail': fail, 'role': Profile.objects.get(user=request.user).role, })
            elif user_profile.role == 'Employee':
                taken = KIATransaction.objects.filter(assigned_emp=Profile.objects.get(user=request.user)).count()
                accepted = KIATransaction.objects.filter(assigned_emp=Profile.objects.get(user=request.user),
                                                         state=KIATransaction.done).count()

                return render(request, 'KIA_services/emp_panel.html',
                              {'taken': taken,
                               'accepted': accepted, 'role': Profile.objects.get(user=request.user).role, })
            return render(request, 'KIA_general/homepage.html', {'role': Profile.objects.get(user=request.user).role, })
    else:
        return render(request, 'KIA_general/homepage.html')


def send_registration_email(email_address):
    subject = 'ثبت‌نام در سامانه KIA_payment'
    message_body = 'ثبت‌نام شما در سامانه کیاپرداخت با موفقیت انجام شد.'
    sender_address = 'kiapayment2018@gmail.com'
    receiver_addresses = [email_address]
    send_mail(subject, message_body, sender_address, receiver_addresses)


def edit_profile(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)

        information = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'account_number': user_profile.account_number,
            'phone_number': user_profile.phone_number,
        }
        if request.method == 'GET':

            return render(request, 'KIA_auth/edit_profile.html',
                          {'information': information, 'role': Profile.objects.get(user=request.user).role, })

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
                # return redirect('edit_profile')
                return render(request, 'KIA_general/success.html',
                              {'message': 'اظلاعات شما با موفقیت ویرایش شد', 'return_url': ''})
            else:
                return render(request, 'KIA_auth/edit_profile.html', {'information': information, 'form': form,
                                                                      'role': Profile.objects.get(
                                                                          user=request.user).role, })

    else:
        return render(request, not_authorized_template)


def user_panel(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)

        total_rial = KIATransaction.objects.filter(user=Profile.objects.get(user=request.user)).aggregate(
            total=Sum('cost_in_rial'))['total']
        cnt = KIATransaction.objects.filter(user=Profile.objects.get(user=request.user)).count()

        information = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'account_number': user_profile.account_number,
            'phone_number': user_profile.phone_number,
            'credit': user_profile.credit,
            'total_rial': total_rial,
            'cnt': cnt
        }

        return render(request, 'KIA_auth/user_panel.html',
                      {'information': information, 'role': Profile.objects.get(user=request.user).role, })
    else:
        return render(request, not_authorized_template)


def change_password(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'KIA_auth/change_password.html',
                          {'role': Profile.objects.get(user=request.user).role, })

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
                        return render(request, 'KIA_general/success.html', {'message': 'رمز عبور شما با موفقیت تغییر یافت', 'return_url': ''})
                    else:
                        errors = {'old password': 'The old password is wrong'}
                        return render(request, 'KIA_auth/change_password.html', {'errors': errors, 'form': form,
                                                                                 'role': Profile.objects.get(
                                                                                     user=request.user).role, })
                else:
                    errors = {'new password': "Passwords doesn't match"}
                    return render(request, 'KIA_auth/change_password.html',
                                  {'errors': errors, 'role': Profile.objects.get(user=request.user).role, })
            else:
                return render(request, 'KIA_auth/change_password.html',
                              {'form': form, 'role': Profile.objects.get(user=request.user).role, })
    else:
        return render(request, not_authorized_template)


def add_credit(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if request.method == 'GET':
            current_credit = user_profile.credit
            return render(request, 'KIA_auth/add_credit.html',
                          {'current_credit': current_credit, 'role': Profile.objects.get(user=request.user).role, })

        elif request.method == 'POST':
            increasing_credit = int(request.POST.get("added_credit"))
            user_profile.credit += increasing_credit
            user_profile.save()
            return redirect('add_credit')
    else:
        return render(request, not_authorized_template)


def withdraw_credit(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if request.method == 'GET':
            current_credit = user_profile.credit
            return render(request, 'KIA_auth/withdraw_credit.html',
                          {'current_credit': current_credit, 'role': Profile.objects.get(user=request.user).role, })

        elif request.method == 'POST':
            withdrawing_credit = int(request.POST.get("sub_credit"))
            user_profile.credit -= withdrawing_credit
            user_profile.save()
            current_credit = user_profile.credit
            return render(request, 'KIA_auth/withdraw_credit.html',
                          {'current_credit': current_credit, 'role': Profile.objects.get(user=request.user).role, })
    else:
        return render(request, not_authorized_template)


def anonymous_transfer(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        current_credit = user_profile.credit

        if request.method == 'GET':
            return render(request, 'KIA_auth/anonymous_transfer.html',
                          {'current_credit': current_credit, 'role': Profile.objects.get(user=request.user).role, })

        elif request.method == 'POST':
            form = AnonymousTransferForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                expired_transfer = request.POST.get("expired")
                print(expired_transfer)
                if expired_transfer == "1":
                    return redirect('anonymous_transfer')
                target_email = cleaned_data.get("email")
                target_account_number = cleaned_data.get("account_number")
                transferring_amount = cleaned_data.get("transfer_credit")

                all_users = User.objects.all()
                account_number_exists = False
                for sys_user in all_users:
                    if sys_user.username == 'iran':
                        continue
                    sys_user_profile = Profile.objects.get(user=sys_user)
                    print(sys_user_profile.account_number)
                    print(sys_user.email)
                    if sys_user_profile.account_number == target_account_number:
                        if sys_user.email == target_email:
                            user_profile.credit -= transferring_amount
                            sys_user_profile.credit += transferring_amount
                            user_profile.save()
                            sys_user_profile.save()
                            send_anonymous_transfer_email(target_email, transferring_amount)
                            return redirect('anonymous_transfer')

                if not account_number_exists:
                    sys_username = random_string_generator(10)
                    sys_password = random_string_generator(16)
                    hashed_password = hashers.make_password(sys_password)
                    sys_user = User.objects.create(username=sys_username, password=hashed_password, email=target_email)
                    sys_user.first_name = 'our user'
                    sys_user.last_name = 'our user'
                    sys_user.save()
                    sys_user_profile = Profile.objects.create(user=sys_user, account_number=target_account_number)
                    sys_user_profile.phone_number = '00000000000'
                    print(transferring_amount)
                    user_profile.credit -= transferring_amount
                    sys_user_profile.credit += transferring_amount
                    user_profile.save()
                    sys_user_profile.save()
                    send_anonymous_transfer_create_account_email(target_email, transferring_amount, sys_username,
                                                                 sys_password)
                    return redirect('anonymous_transfer')

            else:
                return render(request, 'KIA_auth/anonymous_transfer.html',
                              {'form': form, 'current_credit': current_credit,
                               'role': Profile.objects.get(user=request.user).role, })

            return redirect('anonymous_transfer')

    else:
        return render(request, not_authorized_template)


def send_anonymous_transfer_email(email_address, transferring_amount):
    subject = 'پرداخت ناشناس از سامانه KIA_payment'
    message_body = 'در سامانه کیاپرداخت مبلغ %s ریال توسط یکی از کاربران بصورت ناشناس  به کیف پولتان واریز شده است.' % transferring_amount
    sender_address = 'kiapayment2018@gmail.com'
    receiver_addresses = [email_address]
    send_mail(subject, message_body, sender_address, receiver_addresses)


def send_anonymous_transfer_create_account_email(email_address, transferring_amount, username, password):
    subject = 'پرداخت ناشناس از سامانه KIA_payment'
    message_body = 'برای شما در سامانه کیاپرداخت یک حساب کاربری ساخته شده است و مبلغ %s ریال توسط یکی از کاربران بصورت ناشناس  به کیف پولتان واریز شده است.' % transferring_amount
    message_body += '\n'
    message_body += 'username: %s \n' % username
    message_body += 'password: %s \n' % password
    sender_address = 'kiapayment2018@gmail.com'
    receiver_addresses = [email_address]
    send_mail(subject, message_body, sender_address, receiver_addresses)


def transaction_history(request):
    user = None
    if request.user.is_authenticated:
        user = Profile.objects.get(user=request.user)
    else:
        return HttpResponse("Login first")

    registered_transactions = KIATransaction.objects.filter(user=user, state=KIATransaction.registered)
    being_done_transactions = KIATransaction.objects.filter(Q(user=user) &
                                                            (Q(state=KIATransaction.being_done) | Q(
                                                                state=KIATransaction.suspicious)))

    finished_transactions = KIATransaction.objects.filter(user=user, state=KIATransaction.done)
    failed_transactions = KIATransaction.objects.filter(user=user, state=KIATransaction.failed)

    return render(request, 'KIA_auth/transaction_history.html', {'registered': registered_transactions,
                                                                 'being_done': being_done_transactions,
                                                                 'done': finished_transactions,
                                                                 'failed': failed_transactions,
                                                                 'role': Profile.objects.get(user=request.user).role, })


def transaction(request, index):
    if request.user.is_authenticated:
        user = Profile.objects.get(user=request.user)
    else:
        return HttpResponse("Login first")


def random_string_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
