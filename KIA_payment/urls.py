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
from testapp import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('add_feature/', views.add_feature, name='add_feature'),
    path('currency_to_rial/', views.currency_to_rial, name='currency_to_rial'),
    path('get_service_price/', views.get_service_price, name='get_service_price'),
    path('admin/panel', views.admin_panel, name='admin_panel'),
    path('admin/restrict_user', views.admin_restrict_user, name='admin_restrict_user'),
    #login
    path('user_login/', views.user_login, name='user_login'),
    path('employee_login/', views.employee_login, name='employee_login'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin/', admin.site.urls),
]
