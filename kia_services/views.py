import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView, View

from kia_services.forms import KIAServiceForm, KIAServiceCreationForm, KIAServiceFieldCreationForm
from kia_services.models import KIAService, KIATransaction
from KIA_auth.models import Profile


def is_user_admin(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        role = user_profile.role
        if role == 'user':  # TODO: change to admin
            return True
        return False
    return False


def is_user_emp(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        role = user_profile.role
        if role == 'user':  # TODO: change to employee
            return True
        return False
    return False


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
            transaction.username = username
            transaction.data = form.get_json_data()
            transaction.save()
            return HttpResponse("Transaction saved")  # TODO: return a proper response


def admin_service(request, name):
    if not is_user_admin(request):
        return HttpResponse("Not Authorized as admin")

    service = get_object_or_404(KIAService, name=name)

    if request.method == "GET":
        form = KIAServiceForm(service)
        return render(request, 'kia_services/admin_service.html', {'form': form})

    elif request.method == "POST":
        field_form = KIAServiceFieldCreationForm(request.POST)

        if 'delete' in field_form.data:
            return service.delete()
        elif 'augment' in field_form.data:
            return HttpResponseRedirect('/create_service/' + service.name)
        elif 'exclude' in field_form.data:
            return HttpResponseRedirect('fields')


def admin_service_fields(request, name):
    return HttpResponseRedirect("Hello world!")


def create_service(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        role = user_profile.role
        if role == 'user':  # TODO: change this to admin

            if request.method == 'GET':
                form = KIAServiceCreationForm()
                return render(request, 'kia_services/create_service.html', {'form': form})

            elif request.method == "POST":
                service_form = KIAServiceCreationForm(request.POST)
                if service_form.is_valid():
                    new_service = service_form.save()
                    new_service.save()

                    url = new_service.name + "/"

                    return HttpResponseRedirect(url)
                else:
                    # TODO: return a proper response
                    return HttpResponse(service_form.errors)
        # TODO: return proper responses
        else:
            return HttpResponse("Not Authorized as admin")
    else:
        return HttpResponse("Login first")


def create_service_cont(request, name):
    service = get_object_or_404(KIAService, name=name)

    if request.user.is_authenticated:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        role = user_profile.role
        if role == 'user':  # TODO: change this to admin

            if request.method == 'GET':
                form = KIAServiceFieldCreationForm()
                return render(request, 'kia_services/create_service_cont.html', {'form': form})

            elif request.method == "POST":
                field_form = KIAServiceFieldCreationForm(request.POST)

                if field_form.is_valid():
                    new_field = field_form.save()
                    new_field.service = service
                    new_field.save()

                    if 'cont' in field_form.data:
                        return HttpResponseRedirect("")
                    elif 'finish' in field_form.data:
                        return HttpResponse("service saved!")
                    else:
                        return HttpResponse(request.POST.get('action'))
                else:
                    # TODO: return a proper response
                    return HttpResponse(field_form.errors)

        # TODO: return proper responses
        else:
            return HttpResponse("Not Authorized as admin")
    else:
        return HttpResponse("Login first")


class ServiceListView(ListView):
    model = KIAService
    queryset = KIAService.objects.all()
    template_name = 'kia_services/service_list.html'
    context_object_name = 'services'


class AdminServiceListDispatchView(View):
    def dispatch(self, request, *args, **kwargs):
        if is_user_admin(request):
            return AdminServiceListView.as_view()(request, *args, *kwargs)
        else:
            return HttpResponse("Not Authorized as admin")


class AdminServiceListView(ListView):
    model = KIAService
    queryset = KIAService.objects.all()
    template_name = 'kia_services/admin_service_list.html'
    context_object_name = 'services'


class EmpTransactionListView(ListView):
    model = KIATransaction
    queryset = KIATransaction.objects.filter(state=KIATransaction.registered)
    template_name = 'kia_services/emp_transaction_list.html'
    context_object_name = 'transactions'


def emp_transaction(request, index):
    if not is_user_emp(request):
        return HttpResponse("Forbidden")

    transaction = get_object_or_404(KIATransaction, id=index)
    decoded_data = json.loads(transaction.data)

    if request.method == "GET":
        return render(request, 'kia_services/emp_transaction.html'
                      , {'transaction': transaction, 'data': decoded_data})
