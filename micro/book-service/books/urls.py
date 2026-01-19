from django.urls import path
from . import views

urlpatterns = [
    path('api/books/', views.book_list, name='book_list'),
    path('api/books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('api/books/<int:book_id>/stock/', views.update_stock, name='update_stock'),
]
