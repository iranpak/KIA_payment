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
        if user_profile.role == 'Admin':
            if request.method == 'GET':
                return render(request, 'KIA_notification/send_email_by_employee.html')
            elif request.method == 'POST':
                subject = request.POST.get('subject')
                message_body = request.POST.get('message_body')
                sender_address = 'kiapayment2018@gmail.com'
                receiver_username = request.POST.get('receiver_username')
                receiver_user = User.objects.get(username=receiver_username)
                receiver_addresses = [receiver_user.email]
                send_mail(subject, message_body, sender_address, receiver_addresses)
                return redirect('emp_panel')
        else:
            return render(request, access_denied_template)
    else:
        return render(request, not_authorized_template)

