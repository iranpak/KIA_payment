from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_us, name='contact_us'),
    path('', views.register, name='register'),
    path('', views.add_feature, name='add_feature'),
    path('', views.currency_to_rial, name='currency_to_rial'),
    path('', views.get_service_price, name='get_service_price'),
    #login
    path('', views.user_login, name='user_login'),
    path('', views.employee_login, name='employee_login'),
    path('', views.admin_login, name='admin_login'),
]