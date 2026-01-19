# Infrastructure Layer - Django ORM Models
from django.db import models

class CustomerModel(models.Model):
    """Django ORM model for Customer"""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'infrastructure_customer'
    
    def __str__(self):
        return self.name


class BookModel(models.Model):
    """Django ORM model for Book"""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'infrastructure_book'
    
    def __str__(self):
        return self.title


class CartModel(models.Model):
    """Django ORM model for Cart"""
    customer_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'infrastructure_cart'
    
    def __str__(self):
        return f"Cart {self.id}"


class CartItemModel(models.Model):
    """Django ORM model for CartItem"""
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='items')
    book_id = models.IntegerField()
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'infrastructure_cartitem'
        unique_together = ('cart', 'book_id')
    
    def __str__(self):
        return f"CartItem {self.id}"
