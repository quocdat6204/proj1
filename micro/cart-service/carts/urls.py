from django.urls import path
from . import views

urlpatterns = [
    path('api/carts/', views.create_cart, name='create_cart'),
    path('api/carts/<int:cart_id>/', views.get_cart, name='get_cart'),
    path('api/carts/<int:cart_id>/items/', views.add_item, name='add_item'),
    path('api/carts/<int:cart_id>/items/<int:item_id>/', views.remove_item, name='remove_item'),
]
