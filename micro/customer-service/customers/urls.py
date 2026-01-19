from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.register, name='register'),
    path('api/login/', views.login, name='login'),
    path('api/customers/<int:customer_id>/', views.get_customer, name='get_customer'),
]
