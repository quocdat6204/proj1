# Use Cases Layer - Application business rules
import hashlib
from domain.entities.customer import Customer

class CustomerUseCases:
    """Use cases for customer operations"""
    
    def __init__(self, customer_repository):
        self.customer_repository = customer_repository
    
    def register_customer(self, name, email, password):
        """Register a new customer"""
        # Create customer entity
        customer = Customer(name=name, email=email, password=password)
        
        # Validate
        customer.validate()
        
        # Check if email already exists
        existing = self.customer_repository.find_by_email(email)
        if existing:
            raise ValueError("Email already registered")
        
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        customer.password = hashed_password
        
        # Save to repository
        return self.customer_repository.save(customer)
    
    def login_customer(self, email, password):
        """Login customer"""
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Find customer
        customer = self.customer_repository.find_by_email(email)
        
        if not customer or customer.password != hashed_password:
            raise ValueError("Invalid email or password")
        
        return customer
    
    def get_customer_by_id(self, customer_id):
        """Get customer by ID"""
        return self.customer_repository.find_by_id(customer_id)
