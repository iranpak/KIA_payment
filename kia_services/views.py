from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from kia_services.forms import KIAServiceForm
from kia_services.models import KIAService, KIATransaction


def services(request, name):
    service = get_object_or_404(KIAService, name=name)

    authenticated = False
    username = None
    if request.user.is_authenticated:
        authenticated = True
        username = request.user.username

    if request.method == "GET":
        form = KIAServiceForm(service)
        return render(request, 'kia_services/service.html', {'form': form, 'authenticated': authenticated})

    elif request.method == "POST":
        form = KIAServiceForm(service, request.POST)
        if form.is_valid():
            transaction = KIATransaction()
            transaction.initialize(service.name)

            transaction.data = form.get_json_data()
            transaction.save()
            return HttpResponse("Transaction saved")


