# Domain Layer - Pure business entities with no dependencies

class Customer:
    """Customer entity representing a bookstore customer"""
    
    def __init__(self, id=None, name='', email='', password=''):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
    
    def validate(self):
        """Validate customer data"""
        if not self.name:
            raise ValueError("Name is required")
        if not self.email:
            raise ValueError("Email is required")
        if '@' not in self.email:
            raise ValueError("Invalid email format")
        if len(self.password) < 6:
            raise ValueError("Password must be at least 6 characters")
        return True
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
