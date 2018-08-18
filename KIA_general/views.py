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




