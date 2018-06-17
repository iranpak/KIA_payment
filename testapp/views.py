from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def register(request):
    context = {}
    template = loader.get_template('testapp/register.html')
    return HttpResponse(template.render(context, request))


def contact_us(request):
    context = {}
    template = loader.get_template('testapp/contact_us.html')
    return HttpResponse(template.render(context, request))


def add_feature(request):
    context = {}
    template = loader.get_template('testapp/add_feature.html')
    return HttpResponse(template.render(context, request))


def currency_to_rial(request):
    context = {}
    template = loader.get_template('testapp/currency_to_rial.html')
    return HttpResponse(template.render(context, request))


def get_service_price(request):
    context = {}
    template = loader.get_template('testapp/get_service_price.html')
    return HttpResponse(template.render(context, request))


# login
def user_login(request):
    context = {}
    template = loader.get_template('testapp/user_login.html')
    return HttpResponse(template.render(context, request))


def employee_login(request):
    context = {}
    template = loader.get_template('testapp/employee_login.html')
    return HttpResponse(template.render(context, request))


def admin_login(request):
    context = {}
    template = loader.get_template('testapp/admin_login.html')
    return HttpResponse(template.render(context, request))


def admin_panel(request):
    context = {}
    template = loader.get_template('testapp/admin_panel.html')
    return HttpResponse(template.render(context, request))


def admin_restrict_user(request):
    context = {}
    template = loader.get_template('testapp/restrict_user.html')
    return HttpResponse(template.render(context, request))


# Create your views here.
