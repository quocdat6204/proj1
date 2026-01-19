from django.db import models
from accounts.models import Customer
from books.models import Book

class Cart(models.Model):
    customer_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'cart_cart'
    
    def __str__(self):
        return f"Cart {self.id} - Customer {self.customer_id}"
    
    @property
    def items(self):
        return CartItem.objects.filter(cart=self)
    
    @property
    def total_price(self):
        total = sum(item.subtotal for item in self.items)
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    book_id = models.IntegerField()
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'cart_cartitem'
        unique_together = ('cart', 'book_id')
    
    @property
    def book(self):
        return Book.objects.get(id=self.book_id)
    
    @property
    def subtotal(self):
        return self.book.price * self.quantity
    
    def __str__(self):
        return f"CartItem {self.id} - Book {self.book_id}"
