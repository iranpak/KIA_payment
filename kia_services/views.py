from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from kia_services.forms import KIAServiceForm
from kia_services.models import KIAService, KIATransaction
from KIA_auth.models import Profile


def services(request, name):
    service = get_object_or_404(KIAService, name=name)

    if request.method == "GET":
        form = KIAServiceForm(service)
        return render(request, 'kia_services/service.html', {'form': form})

    elif request.method == "POST":
        form = KIAServiceForm(service, request.POST)
        if form.is_valid():
            transaction = KIATransaction()
            transaction.initialize(service.name)
            # TODO: give user login to transaction
            transaction.data = form.get_json_data()
            transaction.save()
            return HttpResponse("Transaction saved")


def increase_balance(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'GET':
            # TODO: show a field for increasing balance
            pass
        elif request.method == 'POST':
            increasing_balance_amount = request.POST.get("increasing_balance_amount")
            user_profile = Profile.objects.get(user=user)
            user_profile.balance += increasing_balance_amount
            user_profile.save()

    else:
        return HttpResponse("not authorized")


def settle_part_of_balance_to_account_number(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'GET':
            # TODO: show a field for enter settling amount
            pass
        elif request.method == 'POST':
            settling_amount = request.POST.get("settling_amount")
            user_profile = Profile.objects.get(user=user)
            if settling_amount > user_profile.balance:
                # TODO: show message for lack of balance
                pass
            else:
                user_profile.balance -= settling_amount

    else:
        return HttpResponse("not authorized")


