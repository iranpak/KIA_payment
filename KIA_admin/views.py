from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from KIA_auth.models import Profile
from django.template import loader


def restrict_user(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if user_profile.role == 'Admin':
            # TODO: show field for restricting user
            user_profile.is_restricted = True
            user_profile.save()
            return HttpResponse("user restricted")

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
            return HttpResponse("user restriction removed")
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
