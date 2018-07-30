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
from test_app import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('contact_us/', views.contact_us, name='contact_us'),
    # admin
    path('add_feature/', views.add_feature, name='add_feature'),
    path('currency_exchange/', views.currency_exchange, name='currency_exchange'),
    path('admin/panel', views.admin_panel, name='admin_panel'),
    path('admin/restrict_user', views.admin_restrict_user, name='admin_restrict_user'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    # login
    path('user_login/', views.user_login, name='user_login'),
    path('employee_login/', views.employee_login, name='employee_login'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin/', admin.site.urls),
    # user
    path('user_profile/', views.user_profile, name='user_profile'),
    path('user_transactions/', views.user_transactions, name='user_transactions'),
    path('user_wallet/', views.user_wallet, name='user_wallet'),
    path('services/physical_mastercard/', views.physical_mastercard, name='physical_mastercard'),
    path('return_money/', views.return_money, name='return_money'),
    path('anonymous_money/', views.anonymous_money, name='anonymous_money'),
    # employee
    path('all_transactions/', views.all_transactions, name='all_transactions'),
    path('all_transactions/1234', views.sample_transaction, name='sample_transaction'),
    path('send_email/', views.send_email, name='send_email'),
    # homepage
    path('homepage/', views.homepage, name='homepage'),
    path('services/', views.services, name='services'),
]
