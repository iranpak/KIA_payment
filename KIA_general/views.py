from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.


def about(request):
    context = {}
    template = loader.get_template('KIA_general/about.html')
    return HttpResponse(template.render(context, request))


def contact_us(request):
    context = {}
    template = loader.get_template('KIA_general/contact_us.html')
    return HttpResponse(template.render(context, request))


def not_found(request):
    context = {}
    template = loader.get_template('KIA_general/404.html')
    return HttpResponse(template.render(context, request))


def not_authorized(request):
    context = {}
    template = loader.get_template('KIA_general/not_authorized.html')
    return HttpResponse(template.render(context, request))


def access_denied(request):
    context = {}
    template = loader.get_template('KIA_general/access_denied.html')
    return HttpResponse(template.render(context, request))


def user_restricted(request):
    context = {}
    template = loader.get_template('KIA_general/user_restricted.html')
    return HttpResponse(template.render(context, request))

