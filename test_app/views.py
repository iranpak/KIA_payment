from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from kia_services.forms import KIAServiceForm
from kia_services.models import KIAService


def register(request):
    context = {}
    template = loader.get_template('test_app/register.html')
    return HttpResponse(template.render(context, request))


def contact_us(request):
    context = {}
    template = loader.get_template('test_app/contact_us.html')
    return HttpResponse(template.render(context, request))


def add_feature(request):
    context = {}
    template = loader.get_template('test_app/add_feature.html')
    return HttpResponse(template.render(context, request))


def currency_exchange(request):
    context = {}
    template = loader.get_template('test_app/currency_exchange.html')
    return HttpResponse(template.render(context, request))


# login
def user_login(request):
    context = {}
    template = loader.get_template('test_app/user_login.html')
    return HttpResponse(template.render(context, request))


def employee_login(request):
    context = {}
    template = loader.get_template('test_app/employee_login.html')
    return HttpResponse(template.render(context, request))


def admin_login(request):
    context = {}
    template = loader.get_template('test_app/admin_login.html')
    return HttpResponse(template.render(context, request))


def admin_panel(request):
    context = {}
    template = loader.get_template('test_app/admin_panel.html')
    return HttpResponse(template.render(context, request))


def admin_restrict_user(request):
    context = {}
    template = loader.get_template('test_app/restrict_user.html')
    return HttpResponse(template.render(context, request))


def user_profile(request):
    context = {}
    template = loader.get_template('test_app/user_profile.html')
    return HttpResponse(template.render(context, request))


def user_transactions(request):
    context = {}
    template = loader.get_template('test_app/user_transactions.html')
    return HttpResponse(template.render(context, request))


def user_wallet(request):
    context = {}
    template = loader.get_template('test_app/user_wallet.html')
    return HttpResponse(template.render(context, request))


def physical_mastercard(request):
    context = {}
    template = loader.get_template('test_app/physical_mastercard.html')
    return HttpResponse(template.render(context, request))


def return_money(request):
    context = {}
    template = loader.get_template('test_app/return_money.html')
    return HttpResponse(template.render(context, request))


def anonymous_money(request):
    context = {}
    template = loader.get_template('test_app/anonymous_money.html')
    return HttpResponse(template.render(context, request))


def all_transactions(request):
    context = {}
    template = loader.get_template('test_app/all_transactions.html')
    return HttpResponse(template.render(context, request))


def sample_transaction(request):
    context = {}
    template = loader.get_template('test_app/sample_transaction.html')
    return HttpResponse(template.render(context, request))


def send_email(request):
    context = {}
    template = loader.get_template('test_app/send_email.html')
    return HttpResponse(template.render(context, request))


def homepage(request):
    context = {}
    template = loader.get_template('test_app/homepage.html')
    return HttpResponse(template.render(context, request))


def add_transaction(request):
    context = {}
    template = loader.get_template('test_app/add_transaction.html')
    return HttpResponse(template.render(context, request))
