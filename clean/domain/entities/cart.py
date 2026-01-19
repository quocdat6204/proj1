# Domain Layer - Cart entities

class CartItem:
    """Cart item entity"""
    
    def __init__(self, id=None, cart_id=None, book_id=None, quantity=1):
        self.id = id
        self.cart_id = cart_id
        self.book_id = book_id
        self.quantity = quantity
    
    def validate(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        return True
    
    def calculate_subtotal(self, book_price):
        """Calculate subtotal for this item"""
        return book_price * self.quantity
    
    def to_dict(self):
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'book_id': self.book_id,
            'quantity': self.quantity
        }


class Cart:
    """Cart entity"""
    
    def __init__(self, id=None, customer_id=None, items=None):
        self.id = id
        self.customer_id = customer_id
        self.items = items or []
    
    def add_item(self, cart_item):
        """Add item to cart"""
        # Check if item already exists
        for item in self.items:
            if item.book_id == cart_item.book_id:
                item.quantity += cart_item.quantity
                return
        self.items.append(cart_item)
    
    def remove_item(self, book_id):
        """Remove item from cart"""
        self.items = [item for item in self.items if item.book_id != book_id]
    
    def calculate_total(self, book_prices):
        """Calculate total price of all items"""
        total = 0
        for item in self.items:
            if item.book_id in book_prices:
                total += item.calculate_subtotal(book_prices[item.book_id])
        return total
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'items': [item.to_dict() for item in self.items]
        }
