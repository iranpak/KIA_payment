from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User
from KIA_auth.models import Profile
from django.shortcuts import redirect


access_denied_template = 'KIA_general/access_denied.html'
not_authorized_template = 'KIA_general/not_authorized.html'


def send_email_by_employee(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if user_profile.role == 'Employee' or user_profile.role == 'Admin':
            if request.method == 'GET':
                return render(request, 'KIA_notification/send_email_by_employee.html', {'role': Profile.objects.get(user=request.user).role})
            elif request.method == 'POST':
                subject = request.POST.get('subject')
                message_body = request.POST.get('message_body')
                sender_address = 'kiapayment2018@gmail.com'
                receiver_username = request.POST.get('receiver_username')
                try:
                    receiver_user = User.objects.get(username=receiver_username)
                    receiver_addresses = [receiver_user.email]
                    send_mail(subject, message_body, sender_address, receiver_addresses)
                    return render(request, 'KIA_general/success.html', {'message': 'ایمیل با موفقیت برای کاربر ارسال شد', 'return_url': ''})
                except Exception as e:
                    errors = {'نام کاربری': 'کاربری با این نام کاربری در سامانه وجود ندارد'}
                    return render(request, 'KIA_notification/send_email_by_employee.html', {'errors': errors})
        else:
            return render(request, access_denied_template, {'role': Profile.objects.get(user=request.user).role})
    else:
        return render(request, not_authorized_template)


def send_mail_to_user(user, subject, message):
    sender_address = 'kiapayment2018@gmail.com'
    email_address = [user.user.email]
    send_mail(subject, message, sender_address, email_address)


def send_mail_to_all_users(subject, message):
    users = Profile.objects.all()
    for user in users:
        send_mail_to_user(user, subject, message)


def send_mail_to_admin(subject, message):
    admin = Profile.objects.get(role="Admin")
    message