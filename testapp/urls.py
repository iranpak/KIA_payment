from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_manager, name='contact_manager'),
    path('', views.register, name='register'),
]