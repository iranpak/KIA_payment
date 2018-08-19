from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.


def admin_panel(request):
    context = {}
    template = loader.get_template('KIA_admin/admin_panel.html')
    return HttpResponse(template.render(context, request))
