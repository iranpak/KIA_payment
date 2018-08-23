from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from KIA_auth.models import Profile
from .models import SystemCredit
from django.template import loader


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
            context = {}
            template = loader.get_template('KIA_general/access_denied.html')
            return HttpResponse(template.render(context, request))
            # return HttpResponse("Access Denied")
    else:
        context = {}
        template = loader.get_template('KIA_general/not_authorized.html')
        return HttpResponse(template.render(context, request))
        # return HttpResponse("not authorized")


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
            # return HttpResponse("user restriction removed")
        else:
            context = {}
            template = loader.get_template('KIA_general/access_denied.html')
            return HttpResponse(template.render(context, request))
            # return HttpResponse("Access Denied")
    else:
        context = {}
        template = loader.get_template('KIA_general/not_authorized.html')
        return HttpResponse(template.render(context, request))
        # return HttpResponse("not authorized")


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
    # context = {}
    # template = loader.get_template('KIA_admin/users_activities.html')
    # return HttpResponse(template.render(context, request))


def employees_activities(request):
    context = {}
    template = loader.get_template('KIA_admin/employees_activities.html')
    return HttpResponse(template.render(context, request))


def my_history(request):
    context = {}
    template = loader.get_template('KIA_admin/my_history.html')
    return HttpResponse(template.render(context, request))


def financial_account_details(request):
    context = {}
    template = loader.get_template('KIA_admin/financial_account_details.html')
    return HttpResponse(template.render(context, request))


def add_system_credit(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if user_profile.role == 'Admin':
            if request.method == 'GET':
                # TODO: show field for restricting user
                return HttpResponse("TODO")
            elif request.method == 'POST':
                increasing_credit = request.POST.get("added_credit")
                system_credit = SystemCredit.objects.get(owner='system')
                system_credit.rial_credit += increasing_credit
                system_credit.save()
        else:
            context = {}
            template = loader.get_template('KIA_general/access_denied.html')
            return HttpResponse(template.render(context, request))
    else:
        context = {}
        template = loader.get_template('KIA_general/not_authorized.html')
        return HttpResponse(template.render(context, request))


def add_transaction(request):
    context = {}
    template = loader.get_template('KIA_admin/add_transaction.html')
    return HttpResponse(template.render(context, request))


