import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from KIA_services.forms import KIAServiceForm
from KIA_services.models import KIAService, KIATransaction, KIAServiceField
from KIA_auth.models import Profile
from KIA_services.forms import KIAServiceForm
from django.views.generic.list import ListView, View
from django.contrib.auth.models import User

from KIA_services.forms import KIAServiceForm, KIAServiceCreationForm, KIAServiceFieldCreationForm
from KIA_services.models import KIAService, KIATransaction
from KIA_auth.models import Profile
from KIA_auth.models import Profile


access_denied_template = 'KIA_general/access_denied.html'
not_authorized_template = 'KIA_general/not_authorized.html'


def is_user_admin(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        role = user_profile.role
        if role == 'Admin':
            return True
        return False
    return False


def is_user_emp(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        role = user_profile.role
        if role == 'Employee':
            return True
        return False
    return False


def get_exchange_rates():
    return {
        1: 80000,
        2: 90000,
        3: 100000,
    }


def services(request, name):
    service = get_object_or_404(KIAService, name=name)

    authenticated = False
    user = None
    if request.user.is_authenticated:
        authenticated = True
        user = Profile.objects.get(user=request.user)

    if request.method == "GET":
        form = KIAServiceForm(service)
        return render(request, 'KIA_services/service.html',
                      {'form': form, 'authenticated': authenticated,
                       'service': service})

    elif request.method == "POST":
        form = KIAServiceForm(service, request.POST)
        if form.is_valid():
            error = None
            if pay_from_user_credit(service, user, form.get_json_data()):
                transaction = KIATransaction()
                transaction.initialize(service)
                user_profile = Profile.objects.get(user=user)
                transaction.user = user_profile
                transaction.data = form.get_json_data()
                transaction.save()
                transaction.assigned_emp = None
                # TODO: send mail to user
                return HttpResponse("Transaction saved")  # TODO: return a proper response
            else:
                error = 'اعتبار شما برای درخواست این خدمت کافی نیست'
                form = KIAServiceForm(service)
                return render(request, 'KIA_services/service.html',
                              {'form': form, 'authenticated': authenticated,
                               'service': service, 'error': error})
        return render(request, 'KIA_services/service.html',
                      {'form': form, 'authenticated': authenticated,
                               'service': service})


def pay_from_user_credit(service, user, json_data):
    cost = None
    if service.variable_price:
        decoded_data = json.loads(json_data)
        cost = get_exchange_rates()[service.currency] * decoded_data['price']
    else:
        cost = get_exchange_rates()[service.currency] * service.price

    if user.credit >= cost:
        user.credit -= cost
        user.save()
        return True
    return False


def admin_service(request, name):
    user = request.user
    if not user.is_authenticated:
        return render(request, not_authorized_template)
    if not is_user_admin(request):
        return render(request, access_denied_template)

    service = get_object_or_404(KIAService, name=name)

    if request.method == "GET":
        form = KIAServiceForm(service)
        return render(request, 'KIA_services/admin_service.html', {'form': form})

    elif request.method == "POST":
        if 'delete' in request.POST:
            return service.delete()
        elif 'augment' in request.POST:
            return HttpResponseRedirect('/create_service/' + service.name)
        elif 'exclude' in request.POST:
            return HttpResponseRedirect('fields')


def admin_service_fields(request, name):
    return HttpResponseRedirect("Hello world!")


def create_service(request):
    if request.user.is_authenticated:
        form = KIAServiceCreationForm()

        if is_user_admin(request):
            if request.method == 'GET':
                return render(request, 'KIA_services/create_service.html', {'form': form})

            elif request.method == "POST":
                service_form = KIAServiceCreationForm(request.POST)
                if service_form.is_valid():
                    new_service = service_form.save()

                    if (not new_service.variable_price) and (new_service.price is None):
                        error = "قیمت خدمت را وارد کنید"
                        return render(request, 'KIA_services/create_service.html',
                                      {'form': form, 'error': error})
                    if new_service.variable_price:
                        price_field = KIAServiceField()
                        price_field.service = new_service
                        price_field.name = "price"
                        price_field.label = "مبلغ پرداختی"
                        price_field.type = KIAServiceField.cost_field
                        price_field.optional = False
                        price_field.args = None
                    new_service.save()
                    url = new_service.name + "/"

                    return HttpResponseRedirect(url)
                else:
                    # TODO: return a proper response
                    return HttpResponse(service_form.errors)
        # TODO: return proper responses
        else:
            return render(request, access_denied_template)
    else:
        return render(request, not_authorized_template)


def create_service_cont(request, name):
    service = get_object_or_404(KIAService, name=name)

    if request.user.is_authenticated:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        role = user_profile.role
        if is_user_admin(request):  # TODO: change this to admin

            if request.method == 'GET':
                form = KIAServiceFieldCreationForm()
                return render(request, 'KIA_services/create_service_cont.html', {'form': form})

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
                return render(request, access_denied_template)
        else:
            return render(request, not_authorized_template)


class ServiceListView(ListView):
    model = KIAService
    queryset = KIAService.objects.all()
    template_name = 'KIA_services/service_list.html'
    context_object_name = 'services'


class AdminServiceListDispatchView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, not_authorized_template)

        if is_user_admin(request):
            return AdminServiceListView.as_view()(request, *args, *kwargs)
        else:
            return render(request, access_denied_template)


class AdminServiceListView(ListView):
    model = KIAService
    queryset = KIAService.objects.all()
    template_name = 'KIA_services/admin_service_list.html'
    context_object_name = 'services'


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
        return render(request, not_authorized_template)


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
        return render(request, not_authorized_template)


class EmpTransactionListDispatchView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, not_authorized_template)
        if is_user_emp(request):
            return EmpTransactionListView.as_view()(request, *args, *kwargs)
        else:
            return render(request, access_denied_template)


class EmpTransactionListView(ListView):
    model = KIATransaction
    queryset = KIATransaction.objects.filter(state=KIATransaction.registered)
    template_name = 'KIA_services/emp_transaction_list.html'
    context_object_name = 'transactions'


def emp_transaction(request, index):
    if not request.user.is_authenticated:
        return render(request, not_authorized_template)
    if not is_user_emp(request):
        return render(request, access_denied_template)

    transaction = get_object_or_404(KIATransaction, id=index)
    decoded_data = json.loads(transaction.data)

    user = request.user
    user_profile = Profile.objects.get(user=user)

    if request.method == "GET":
        return render(request, 'KIA_services/emp_transaction.html'
                      , {'transaction': transaction, 'data': decoded_data, 'user': user_profile})

    # TODO: decorate problem happened s
    elif request.method == 'POST':
        if "take" in request.POST:

            if transaction.assigned_emp is None:
                transaction.assigned_emp = user_profile
                transaction.state = transaction.being_done
                transaction.save()
            else:
                return HttpResponse("A problem happened")

        elif 'finish' in request.POST:

            if transaction.assigned_emp == user_profile:
                transaction.state = transaction.done
                transaction.save()
                # TODO: send mail to user
            else:
                return HttpResponse("A problem happened")

        elif 'report' in request.POST:

            if transaction.assigned_emp == user_profile:
                transaction.state = transaction.suspicious
                transaction.save()
            else:
                return HttpResponse("A problem happened")

        else:
            return HttpResponse(request.POST)

        return HttpResponse("Successful")


def emp_taken_transactions(request):
    if not request.user.is_authenticated:
        return render(request, not_authorized_template)
    if not is_user_emp(request):
        return render(request, access_denied_template)

    user = request.user
    user_profile = Profile.objects.get(user=user)

    being_done_transactions = KIATransaction.objects.filter(assigned_emp=user_profile
                                                            , state=KIATransaction.being_done)
    finished_transactions = KIATransaction.objects.filter(assigned_emp=user_profile
                                                          , state=KIATransaction.done)

    return render(request, 'KIA_services/emp_taken_transactions.html'
                  , {'being_done_transactions': being_done_transactions
                      , 'done_transactions': finished_transactions})


def emp_panel(request):
    if not request.user.is_authenticated:
        return render(request, not_authorized_template)
    if not is_user_emp(request):
        return render(request, access_denied_template)

    user = request.user
    user_profile = Profile.objects.get(user=user)

    return render(request, 'KIA_services/emp_panel.html', {'email': user_profile.user.email,
                                                           'name': user_profile.user.first_name})
