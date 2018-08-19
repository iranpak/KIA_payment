from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from KIA_auth.models import Profile


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
            return HttpResponse("Access Denied")
    else:
        return HttpResponse("not authorized")


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
            return HttpResponse("Access Denied")
    else:
        return HttpResponse("not authorized")






