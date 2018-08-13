from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.


def login(request):
    context = {}
    # per = User(first_name="a", last_name="al", email="a@gmial.com", password="123456", phone_number="12345678912")
    # per.save()
    # print(per.email)
    template = loader.get_template('KIA_auth/login.html')
    return HttpResponse(template.render(context, request))


def register(request):
    context = {}
    # per = User(first_name="a", last_name="al", email="a@gmial.com", password="123456", phone_number="12345678912")
    # per.save()
    # print(per.email)
    template = loader.get_template('KIA_auth/register.html')
    return HttpResponse(template.render(context, request))

