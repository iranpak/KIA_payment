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


# Create your views here.
