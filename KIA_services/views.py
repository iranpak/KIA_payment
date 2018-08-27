import datetime
import json
import requests

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from KIA_admin.models import SystemCredit
from KIA_notification.tasks import plan_transaction_expiration
from KIA_notification.views import send_mail_to_user, send_mail_to_all_users
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
                       'service': service, 'currency': get_exchange_rates()[service.currency],
                       'role': Profile.objects.get(user=request.user).role})

    elif request.method == "POST":
        form = KIAServiceForm(service, request.POST)
        if form.is_valid():
            transaction = KIATransaction()
            if pay_from_user_credit(service, transaction, user, form.get_json_data()):
                transaction.initialize(service)
                user_profile = Profile.objects.get(user=user)
                transaction.user = user_profile
                transaction.register_time = datetime.datetime.now()
                transaction.data = form.get_json_data()
                transaction.save()
                transaction.assigned_emp = None
                message = "درخواست شما برای خدمت" + service.label + "با موفقیت ثبت شد"
                send_mail_to_user(user,
                                  "ثبت درخواست موفق",
                                  message)
                return HttpResponseRedirect("success")
            else:
                error = 'اعتبار شما برای درخواست این خدمت کافی نیست'
                form = KIAServiceForm(service)
                return render(request, 'KIA_services/service.html',
                              {'form': form, 'authenticated': authenticated,
                               'service': service, 'error': error, 'role': Profile.objects.get(user=request.user).role})
        return render(request, 'KIA_services/service.html',
                      {'form': form, 'authenticated': authenticated,
                       'service': service, 'role': Profile.objects.get(user=request.user).role})


def services_success(request, name):
    if not request.user.is_authenticated:
        return render(request, not_authorized_template)

    service = get_object_or_404(KIAService, name=name)
    message = "درخواست شما برای خدمت" + service.label + "با موفقیت ثبت شد."
    return_url = "/services"

    return render(request, 'KIA_general/success.html', {'message': message,
                                                        'return_url': return_url,
                                                        'role': Profile.objects.get(user=request.user).role})


def pay_from_user_credit(service, transaction, user, json_data):
    if service.variable_price:
        decoded_data = json.loads(json_data)
        cost = int(round(
            get_exchange_rates()[service.currency] * decoded_data['price'] \
            * (1 + (service.commission / 100.0))
        ))
        transaction.cost_in_currency = decoded_data['price']
    else:
        cost = int(round(
            get_exchange_rates()[service.currency] * service.price \
            * (1 + (service.commission / 100.0))
        ))
        transaction.cost_in_currency = service.price

    if user.credit >= cost:
        user.credit -= cost
        transaction.cost_in_rial = cost
        sc = SystemCredit.objects.get(owner="system")
        sc.rial_credit += cost
        sc.save()
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
        return render(request, 'KIA_services/admin_service.html',
                      {'form': form, 'label': service.label, 'role': Profile.objects.get(user=request.user).role})

    elif request.method == "POST":
        if 'delete' in request.POST:
            service.delete()
            return HttpResponseRedirect("delete/success")
        elif 'augment' in request.POST:
            return HttpResponseRedirect('/create_service/' + service.name)
        elif 'exclude' in request.POST:
            return HttpResponseRedirect('fields')


def admin_service_delete_success(request, name):
    user = request.user
    if not user.is_authenticated:
        return render(request, not_authorized_template)
    if not is_user_admin(request):
        return render(request, access_denied_template)

    service = get_object_or_404(KIAService, name=name)
    message = "سرویس" + service.label + "با موفقیت حذف شد."
    return_url = "/admin/services"
    return render(request, 'KIA_general/success.html', {'message': message,
                                                        'return_url': return_url,
                                                        'role': Profile.objects.get(user=request.user).role})


def admin_service_fields(request, name):
    # TODO: complete this
    return HttpResponseRedirect("Hello world!")


def create_service(request):
    if not request.user.is_authenticated:
        return render(request, not_authorized_template)

    if not is_user_admin(request):
        return render(request, access_denied_template)

    form = KIAServiceCreationForm()

    if request.method == 'GET':
        return render(request, 'KIA_services/create_service.html',
                      {'form': form, 'role': Profile.objects.get(user=request.user).role})

    elif request.method == "POST":
        service_form = KIAServiceCreationForm(request.POST)
        if service_form.is_valid():
            new_service = service_form.save()

            if (not new_service.variable_price) and (new_service.price is None):
                error = "قیمت خدمت را وارد کنید"
                return render(request, 'KIA_services/create_service.html',
                              {'form': form, 'error': error, 'role': Profile.objects.get(user=request.user).role})
            if new_service.variable_price:
                price_field = KIAServiceField()
                price_field.service = new_service
                price_field.name = "price"
                price_field.label = "مبلغ پرداختی"
                price_field.type = KIAServiceField.integer_field
                price_field.optional = False
                price_field.args = None
                price_field.save()
            new_service.save()
            url = new_service.name + "/"

            return HttpResponseRedirect(url)
        else:
            return render(request, 'KIA_services/create_service.html',
                          {'form': service_form, 'role': Profile.objects.get(user=request.user).role})


def create_service_cont(request, name):
    if not request.user.is_authenticated:
        return render(request, not_authorized_template)

    if not is_user_admin(request):
        return render(request, access_denied_template)

    service = get_object_or_404(KIAService, name=name)

    if request.method == 'GET':
        form = KIAServiceFieldCreationForm()
        return render(request, 'KIA_services/create_service_cont.html',
                      {'form': form, 'role': Profile.objects.get(user=request.user).role})

    elif request.method == "POST":
        field_form = KIAServiceFieldCreationForm(request.POST)

        if 'finish' in field_form.data:
            message = "خدمت" + service.label + "به سامانه کیاپرداخت اضافه شده است! بشتابید!"
            send_mail_to_all_users("خدمت جدید!",
                                   message)
            return HttpResponseRedirect("success")

        if field_form.is_valid():
            if 'cont' in field_form.data:
                new_field = field_form.save()
                new_field.service = service
                new_field.save()
                return HttpResponseRedirect("")
            else:
                return HttpResponse(request.POST.get('action'))
        else:
            return render(request, 'KIA_services/create_service_cont.html',
                          {'form': field_form, 'role': Profile.objects.get(user=request.user).role})


def create_service_success(request, name):
    if not request.user.is_authenticated:
        return render(request, not_authorized_template)

    if not is_user_admin(request):
        return render(request, access_denied_template)

    service = get_object_or_404(KIAService, name=name)
    message = "عملیات با موفقیت انجام شد"
    return_url = "/admin/services"
    return render(request, 'KIA_general/success.html', {'message': message,
                                                        'return_url': return_url,
                                                        'role': Profile.objects.get(user=request.user).role})


class HomeListView(ListView):
    model = KIAService
    queryset = KIAService.objects.all()
    template_name = 'KIA_general/homepage.html'
    context_object_name = 'services'


class HomeServiceListDispatchView(View):
    def dispatch(self, request, *args, **kwargs):
        return HomeListView.as_view()(request, *args, *kwargs)


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
            return render(request, access_denied_template, {'role': Profile.objects.get(user=request.user).role})


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
            return render(request, access_denied_template, {'role': Profile.objects.get(user=request.user).role})


class EmpTransactionListView(ListView):
    model = KIATransaction
    queryset = KIATransaction.objects.filter(state=KIATransaction.registered)
    template_name = 'KIA_services/emp_transaction_list.html'
    context_object_name = 'transactions'


def emp_transaction(request, index):
    if not request.user.is_authenticated:
        return render(request, not_authorized_template)
    if not is_user_emp(request):
        return render(request, access_denied_template, {'role': Profile.objects.get(user=request.user).role})

    transaction = get_object_or_404(KIATransaction, id=index)
    decoded_data = json.loads(transaction.data)

    user = request.user
    user_profile = Profile.objects.get(user=user)

    if request.method == "GET":
        return render(request, 'KIA_services/emp_transaction.html'
                      , {'transaction': transaction, 'data': decoded_data, 'user': user_profile,
                         'role': Profile.objects.get(user=request.user).role})

    # TODO: decorate problem happened s
    elif request.method == 'POST':
        if "take" in request.POST:

            if transaction.assigned_emp is None:
                transaction.assigned_emp = user_profile
                transaction.state = transaction.being_done
                transaction.save()
                plan_transaction_expiration(transaction)
                return HttpResponseRedirect("take/success")
            else:
                return HttpResponse("A problem happened")

        elif 'finish' in request.POST:

            if transaction.assigned_emp == user_profile:
                credit = transaction.cost_in_currency
                flag = True

                currency = transaction.service.currency
                sc = SystemCredit.objects.get(owner="system")

                if currency == KIAService.dollar:
                    if credit > sc.dollar_credit:
                        flag = False
                    else:
                        sc.dollar_credit = sc.dollar_credit - credit
                        sc.save()
                elif currency == KIAService.euro:
                    if credit > sc.euro_credit:
                        flag = False
                    else:
                        sc.euro_credit = sc.euro_credit - credit
                        sc.save()
                elif currency == KIAService.pound:
                    if credit > sc.pound_credit:
                        flag = False
                    else:
                        sc.pound_credit = sc.pound_credit - credit
                        sc.save()

                if flag:
                    transaction.state = transaction.done
                    transaction.save()
                    message = "درخواست شما برای خدمت" + transaction.service.label + "با موفقیت انجام شد"
                    send_mail_to_user(transaction.user,
                                      "موفقیت اتمام خدمت", message)
                    return HttpResponseRedirect("finish/success")
                else:
                    error = "موجودی ارزی سامانه برای تکمیل این عملیات کافی نیست."
                    return render(request, 'KIA_services/emp_transaction.html'
                                  , {'transaction': transaction,
                                     'data': decoded_data,
                                     'user': user_profile,
                                     'error': error, 'role': Profile.objects.get(user=request.user).role})
            else:
                return HttpResponse("A problem happened")

        elif 'report' in request.POST:

            if transaction.assigned_emp == user_profile:
                transaction.state = transaction.suspicious
                transaction.save()
                return HttpResponseRedirect("report/success")
            else:
                return HttpResponse("A problem happened")

        elif 'fail' in request.POST:

            if transaction.assigned_emp == user_profile:
                transaction.state = transaction.failed
                transaction.return_money()
                transaction.save()
                message = "متاسفانه درخواست شما برای خدمت" + transaction.service.label + "رد شد."
                send_mail_to_user(transaction.user, "رد درخواست برای خدمت", message)
                return HttpResponseRedirect("fail/success")
            else:
                return HttpResponse("A problem happened")

        else:
            return HttpResponse(request.POST)


def emp_transaction_take_success(request):
    if not request.user.is_authenticated:
        return render(request, not_authorized_template)
    if not is_user_emp(request):
        return render(request, access_denied_template, {'role': Profile.objects.get(user=request.user).role})

    message = "تراکنش با موفقیت برای شما انتخاب شد"
    return_url = "/emp/taken_transactions"
    return render(request, 'KIA_general/success.html', {'message': message,
                                                        'return_url': return_url,
                                                        'role': Profile.objects.get(user=request.user).role})


def emp_transaction_finish_success(request):
    if not request.user.is_authenticated:
        return render(request, not_authorized_template)
    if not is_user_emp(request):
        return render(request, access_denied_template, {'role': Profile.objects.get(user=request.user).role})

    message = "تراکنش با موفقیت به اتمام رسید و " \
              "ایمیلی در همین رابطه برای کاربر مربوط فرستاده شد."
    return_url = "/emp/taken_transactions"
    return render(request, 'KIA_general/success.html', {'message': message,
                                                        'return_url': return_url,
                                                        'role': Profile.objects.get(user=request.user).role})


def emp_transaction_report_success(request):
    if not request.user.is_authenticated:
        return render(request, not_authorized_template)
    if not is_user_emp(request):
        return render(request, access_denied_template, {'role': Profile.objects.get(user=request.user).role})

    message = "تراکنش به عنوان تراکنش مشکوک به مدیر سایت گزارش شد."
    return_url = "/emp/taken_transactions"
    return render(request, 'KIA_general/success.html', {'message': message,
                                                        'return_url': return_url,
                                                        'role': Profile.objects.get(user=request.user).role})


def emp_transaction_fail_success(request):
    if not request.user.is_authenticated:
        return render(request, not_authorized_template)
    if not is_user_emp(request):
        return render(request, access_denied_template, {'role': Profile.objects.get(user=request.user).role})

    message = "تراکنش از سمت شما رد و ایمیلی متناسب با این موضوع برای کاربر مربوط فرستاده شد."
    return_url = "/emp/taken_transactions"
    return render(request, 'KIA_general/success.html', {'message': message,
                                                        'return_url': return_url,
                                                        'role': Profile.objects.get(user=request.user).role})


def emp_taken_transactions(request):
    if not request.user.is_authenticated:
        return render(request, not_authorized_template)
    if not is_user_emp(request):
        return render(request, access_denied_template, {'role': Profile.objects.get(user=request.user).role})

    user = request.user
    user_profile = Profile.objects.get(user=user)

    being_done_transactions = KIATransaction.objects.filter(assigned_emp=user_profile
                                                            , state=KIATransaction.being_done)
    finished_transactions = KIATransaction.objects.filter(assigned_emp=user_profile
                                                          , state=KIATransaction.done)

    suspicious_transactions = KIATransaction.objects.filter(assigned_emp=user_profile,
                                                            state=KIATransaction.suspicious)

    failed_transactions = KIATransaction.objects.filter(assigned_emp=user_profile,
                                                        state=KIATransaction.failed)

    return render(request, 'KIA_services/emp_taken_transactions.html'
                  , {'being_done_transactions': being_done_transactions
                      , 'done_transactions': finished_transactions
                      , 'suspicious_transactions': suspicious_transactions
                      , 'failed_transactions': failed_transactions,
                     'role': Profile.objects.get(user=request.user).role})


def admin_transaction(request, index):
    if not request.user.is_authenticated:
        return render(request, not_authorized_template)
    if not is_user_admin(request):
        return render(request, access_denied_template, {'role': Profile.objects.get(user=request.user).role})

    transaction = get_object_or_404(KIATransaction, id=index)
    decoded_data = json.loads(transaction.data)

    if request.method == "GET":
        return render(request, 'KIA_services/admin_transaction.html'
                      , {'transaction': transaction, 'data': decoded_data,
                         'role': Profile.objects.get(user=request.user).role})

    # TODO: decorate problem happened s
    elif request.method == 'POST':
        if "fail" in request.POST:
            transaction.state = transaction.failed
            transaction.save()

        elif 'return' in request.POST:
            transaction.state = transaction.being_done
            transaction.save()

        else:
            return HttpResponse("A problem happened")

        return HttpResponse("Successful")


def emp_panel(request):
    if not request.user.is_authenticated:
        return render(request, not_authorized_template)
    if not is_user_emp(request):
        return render(request, access_denied_template, {'role': Profile.objects.get(user=request.user).role})

    user = request.user
    user_profile = Profile.objects.get(user=user)

    taken = KIATransaction.objects.filter(assigned_emp=Profile.objects.get(user=request.user)).count()
    accepted = KIATransaction.objects.filter(assigned_emp=Profile.objects.get(user=request.user),
                                             state=KIATransaction.done).count()

    return render(request, 'KIA_services/emp_panel.html', {'email': user_profile.user.email,
                                                           'name': user_profile.user.first_name,
                                                           'username': user_profile.user.username,
                                                           'taken': taken,
                                                           'accepted': accepted,
                                                           'role': Profile.objects.get(user=request.user).role})


def get_exchange_rates():
    try:
        response = requests.get(
            'http://core.arzws.com/api/core?Token=a6d2b63a-5abf-42c0-bdb7-08d609cedc20&what=exchange')
        data = json.loads(response.text)
        all_currency_list = data['currencyBoard']

        our_currency_list = {}
        for currency in all_currency_list:
            if currency['name'] == 'دلار آمریکا تهران':
                our_currency_list[1] = currency['maxVal']
            if currency['name'] == 'یورو':
                our_currency_list[2] = currency['maxVal']
            if currency['name'] == 'پوند انگلیس':
                our_currency_list[3] = currency['maxVal']
    except:
        our_currency_list = {
            1: 105000,
            2: 130000,
            3: 135000,
        }

    return our_currency_list
