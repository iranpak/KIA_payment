"""KIA_payment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from test_app import views as test_app_views
from kia_services import views as kia_services_views
from django.contrib.auth import views as auth_views
from KIA_auth import views as KIA_auth_views
from KIA_general import views as KIA_gen_views
from KIA_admin import views as KIA_admin_views

urlpatterns = [
    path('', KIA_auth_views.redirect_to_home, name='home'),
    # path('', auth_views.auth_login, {'template_name': 'KIA_auth/home.html'}, name='home'),
    path('accounts/profile/', RedirectView.as_view(pattern_name='home')),
    # path('contact_us/', test_app_views.contact_us, name='contact_us'),
    # general
    path('contact_us/', KIA_gen_views.contact_us, name='contact_us'),
    path('about/', KIA_gen_views.about, name='about'),
    path('404/', KIA_gen_views.not_found, name='not_found'),
    path('not_authorized/', KIA_gen_views.not_authorized, name='not_authorized'),
    path('access_denied/', KIA_gen_views.access_denied, name='access_denied'),
    path('user_restricted/', KIA_gen_views.user_restricted, name='user_restricted'),
    path('services/', KIA_gen_views.services, name='services'),
    # admin
    # panels

    path('add_feature/', test_app_views.add_feature, name='add_feature'),
    path('currency_exchange/', test_app_views.currency_exchange, name='currency_exchange'),
    # admin
    # path('admin/panel', test_app_views.admin_panel, name='admin_panel'),
    path('admin/panel', KIA_admin_views.panel, name='admin_panel'),
    path('admin/users_activities', KIA_admin_views.users_activities, name='users_activities'),
    path('admin/employees_activities', KIA_admin_views.employees_activities, name='employees_activities'),
    path('admin/my_history', KIA_admin_views.my_history, name='my_history'),
    path('admin/financial_account_details', KIA_admin_views.financial_account_details,
         name='financial_account_details'),
    path('admin/add_system_credit', KIA_admin_views.add_system_credit, name='add_system_credit'),
    # path('admin/restrict_user', test_app_views.admin_restrict_user, name='admin_restrict_user'),
    path('admin/restrict_user', KIA_admin_views.restrict_user, name='restrict_user'),
    path('admin/remove_user_restriction', KIA_admin_views.remove_user_restriction, name='remove_user_restriction'),
    # path('add_transaction/', test_app_views.add_transaction, name='add_transaction'),
    path('admin/add_transaction/', KIA_admin_views.add_transaction, name='add_transaction'),

    # auth
    path('login/', auth_views.login, {'template_name': 'KIA_auth/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'template_name': 'KIA_auth/logout.html'}, name='logout'),
    path('signup/', KIA_auth_views.sign_up, name='signup'),

    # user panel
    path('edit_profile/', KIA_auth_views.edit_profile, name='edit_profile'),
    path('change_password/', KIA_auth_views.change_password, name='change_password'),
    path('add_credit/', KIA_auth_views.add_credit, name='add_credit'),

    path('employee_login/', test_app_views.employee_login, name='employee_login'),
    path('admin_login/', test_app_views.admin_login, name='admin_login'),
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
    path('all_transactions/1234', test_app_views.sample_transaction, name='sample_transaction'),
    path('send_email/', test_app_views.send_email, name='send_email'),
    # homepage
    path('homepage/', test_app_views.homepage, name='homepage'),
    # kia_services
    path('services/<str:name>/', kia_services_views.services, name='services'),
]
