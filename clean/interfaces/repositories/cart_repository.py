# Interfaces Layer - Cart repository interface
from abc import ABC, abstractmethod

class CartRepository(ABC):
    """Abstract repository for Cart operations"""
    
    @abstractmethod
    def save(self, cart):
        """Save cart"""
        pass
    
    @abstractmethod
    def find_by_id(self, cart_id):
        """Find cart by ID"""
        pass
    
    @abstractmethod
    def find_by_customer_id(self, customer_id):
        """Find cart by customer ID"""
        pass
    
    @abstractmethod
    def add_item(self, cart_id, cart_item):
        """Add item to cart"""
        pass
    
    @abstractmethod
    def remove_item(self, cart_id, item_id):
        """Remove item from cart"""
        pass
    
    @abstractmethod
    def get_items(self, cart_id):
        """Get cart items"""
        pass
