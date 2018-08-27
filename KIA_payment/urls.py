from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from test_app import views as test_app_views
from KIA_services import views as kia_services_views
from django.contrib.auth import views as auth_views
from KIA_auth import views as KIA_auth_views
from KIA_general import views as KIA_gen_views
from KIA_admin import views as KIA_admin_views
from KIA_notification import views as KIA_notif_views

urlpatterns = [
    path('', KIA_auth_views.redirect_to_home, name='home'),
    path('accounts/profile/', RedirectView.as_view(pattern_name='home')),
    # general
    path('contact_us/', KIA_gen_views.contact_us, name='contact_us'),
    path('about/', KIA_gen_views.about, name='about'),
    path('404/', KIA_gen_views.not_found, name='not_found'),
    path('not_authorized/', KIA_gen_views.not_authorized, name='not_authorized'),
    path('access_denied/', KIA_gen_views.access_denied, name='access_denied'),
    path('user_restricted/', KIA_gen_views.user_restricted, name='user_restricted'),
    path('service_info/', KIA_gen_views.service_info, name='service_info'),
    path('purchase/', KIA_gen_views.purchase, name='purchase'),
    path('currency_rates/', KIA_gen_views.currency_rates, name='currency_rates'),
    path('FAQ/', KIA_gen_views.faq, name='faq'),
    path('add_feature/', test_app_views.add_feature, name='add_feature'),
    path('currency_exchange/', test_app_views.currency_exchange, name='currency_exchange'),
    path('send_email/', KIA_notif_views.send_email_by_employee, name='send_email_by_employee'),

    # admin
    path('admin/panel', KIA_admin_views.panel, name='admin_panel'),
    # path('admin/users_activities', KIA_admin_views.users_activities, name='users_activities'),
    # path('admin/employees_activities', KIA_admin_views.employees_activities, name='employees_activities'),
    path('admin/activities', KIA_admin_views.activities, name='activities'),
    path('admin/transactions/<int:index>/', kia_services_views.admin_transaction, name='admin_transaction'),
    path('admin/my_history', KIA_admin_views.my_history, name='my_history'),
    path('admin/financial_account_details', KIA_admin_views.financial_account_details,
         name='financial_account_details'),
    path('admin/add_system_credit', KIA_admin_views.add_system_credit, name='add_system_credit'),
    path('admin/restrict_user', KIA_admin_views.restrict_user, name='restrict_user'),
    path('admin/remove_user_restriction', KIA_admin_views.remove_user_restriction, name='remove_user_restriction'),
    # path('admin/add_transaction/', KIA_admin_views.add_transaction, name='add_transaction'),
    path('admin/add_user', KIA_admin_views.add_user, name='add_user'),
    path('admin/show_system_transactions', KIA_admin_views.show_system_transactions, name='show_system_transactions'),

    path('admin/panel', test_app_views.admin_panel, name='admin_panel'),
    path('admin/restrict_user', test_app_views.admin_restrict_user, name='admin_restrict_user'),
    path('add_transaction/', test_app_views.add_transaction, name='add_transaction'),
    # TODO: must be here or in services?
    path('admin/services/', kia_services_views.AdminServiceListDispatchView.as_view(), name='admin_service_list'),
    path('admin/services/<str:name>', kia_services_views.admin_service, name='admin_service'),
    path('admin/services/<str:name>/fields', kia_services_views.admin_service_fields, name='admin_service_fields'),
    path('admin/services/<str:name>/delete/success'
         , kia_services_views.admin_service_delete_success
         , name='admin_service_delete_success'),
    # auth
    # TODO what is the user is already logged in?
    path('login/', auth_views.login, {'template_name': 'KIA_auth/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'template_name': 'KIA_auth/logout.html'}, name='logout'),
    path('signup/', KIA_auth_views.sign_up, name='signup'),
    # user panel
    path('user_panel/', KIA_auth_views.user_panel, name='edit_profile'),
    path('edit_profile/', KIA_auth_views.edit_profile, name='edit_profile'),
    path('change_password/', KIA_auth_views.change_password, name='change_password'),
    path('add_credit/', KIA_auth_views.add_credit, name='add_credit'),
    path('withdraw_credit/', KIA_auth_views.withdraw_credit, name='withdraw_credit'),
    path('anonymous_transfer/', KIA_auth_views.anonymous_transfer, name='anonymous_transfer'),
    path('transactions/', KIA_auth_views.transaction_history, name='transaction_history'),
    path('transactions/<int:index>/', KIA_auth_views.transaction, name='transaction_history'),

    path('admin/', admin.site.urls),
    # user
    path('user_profile/', test_app_views.user_profile, name='user_profile'),
    path('user_transactions/', test_app_views.user_transactions, name='user_transactions'),
    path('user_wallet/', test_app_views.user_wallet, name='user_wallet'),
    path('services/physical_mastercard/', test_app_views.physical_mastercard, name='physical_mastercard'),
    path('return_money/', test_app_views.return_money, name='return_money'),
    path('anonymous_money/', test_app_views.anonymous_money, name='anonymous_money'),
    # employee
    path('all_transactions/', test_app_views.all_transactions, name='all_transactions'),
    # TODO converted to:
    path('emp/panel/', kia_services_views.emp_panel, name='emp_panel'),
    path('emp/transactions/', kia_services_views.EmpTransactionListDispatchView.as_view(), name='emp_transactions'),
    path('all_transactions/1234', test_app_views.sample_transaction, name='sample_transaction'),
    # TODO converted to:
    path('emp/transactions/<int:index>/', kia_services_views.emp_transaction, name='emp_transaction'),
    path('emp/taken_transactions', kia_services_views.emp_taken_transactions, name='emp_taken_transactions'),
    path('send_email/', test_app_views.send_email, name='send_email'),
    # homepage
    # path('homepage/', test_app_views.homepage, name='homepage'),
    path('homepage/', kia_services_views.HomeListView.as_view(), name='homepage'),
    # KIA_services
    path('services/<str:name>/', kia_services_views.services, name='services'),
    path('services/<str:name>/success', kia_services_views.services_success, name='services_success'),
    path('create_service/', kia_services_views.create_service, name='service_creation'),
    path('create_service/<str:name>/', kia_services_views.create_service_cont, name='create_service_cont'),
    path('create_service/<str:name>/success', kia_services_views.create_service_success, name='create_service_success'),
    path('services/', kia_services_views.ServiceListView.as_view(), name='service_list'),
    # tinymce
    # re_path(r'^tinymce/', include('tinymce.urls'))
]
