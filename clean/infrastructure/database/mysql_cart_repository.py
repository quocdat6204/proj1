# Infrastructure Layer - MySQL Cart Repository Implementation
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from interfaces.repositories.cart_repository import CartRepository
from domain.entities.cart import Cart, CartItem
from infrastructure.models import CartModel, CartItemModel

class MySQLCartRepository(CartRepository):
    """MySQL implementation of Cart repository using Django ORM"""
    
    def save(self, cart):
        """Save cart to database"""
        cart_model = CartModel(customer_id=cart.customer_id)
        cart_model.save()
        cart.id = cart_model.id
        return cart
    
    def find_by_id(self, cart_id):
        """Find cart by ID"""
        try:
            model = CartModel.objects.get(id=cart_id)
            return self._to_entity(model)
        except CartModel.DoesNotExist:
            return None
    
    def find_by_customer_id(self, customer_id):
        """Find cart by customer ID"""
        try:
            model = CartModel.objects.get(customer_id=customer_id)
            return self._to_entity(model)
        except CartModel.DoesNotExist:
            return None
    
    def add_item(self, cart_id, cart_item):
        """Add item to cart"""
        cart_model = CartModel.objects.get(id=cart_id)
        
        # Check if item already exists
        try:
            item_model = CartItemModel.objects.get(cart=cart_model, book_id=cart_item.book_id)
            item_model.quantity += cart_item.quantity
            item_model.save()
        except CartItemModel.DoesNotExist:
            item_model = CartItemModel(
                cart=cart_model,
                book_id=cart_item.book_id,
                quantity=cart_item.quantity
            )
            item_model.save()
        
        cart_item.id = item_model.id
        return cart_item
    
    def remove_item(self, cart_id, item_id):
        """Remove item from cart"""
        try:
            item = CartItemModel.objects.get(id=item_id, cart_id=cart_id)
            item.delete()
            return True
        except CartItemModel.DoesNotExist:
            return False
    
    def get_items(self, cart_id):
        """Get cart items"""
        items = CartItemModel.objects.filter(cart_id=cart_id)
        return [self._item_to_entity(item) for item in items]
    
    def _to_entity(self, model):
        """Convert Django model to domain entity"""
        items = self.get_items(model.id)
        return Cart(
            id=model.id,
            customer_id=model.customer_id,
            items=items
        )
    
    def _item_to_entity(self, model):
        """Convert cart item model to entity"""
        return CartItem(
            id=model.id,
            cart_id=model.cart_id,
            book_id=model.book_id,
            quantity=model.quantity
        )
