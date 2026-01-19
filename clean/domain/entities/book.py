# Domain Layer - Book entity

class Book:
    """Book entity representing a book in the store"""
    
    def __init__(self, id=None, title='', author='', price=0.0, stock=0):
        self.id = id
        self.title = title
        self.author = author
        self.price = price
        self.stock = stock
    
    def validate(self):
        """Validate book data"""
        if not self.title:
            raise ValueError("Title is required")
        if not self.author:
            raise ValueError("Author is required")
        if self.price <= 0:
            raise ValueError("Price must be greater than 0")
        if self.stock < 0:
            raise ValueError("Stock cannot be negative")
        return True
    
    def is_available(self):
        """Check if book is available in stock"""
        return self.stock > 0
    
    def reduce_stock(self, quantity):
        """Reduce stock by quantity"""
        if quantity > self.stock:
            raise ValueError("Not enough stock available")
        self.stock -= quantity
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'price': float(self.price),
            'stock': self.stock
        }
