# Infrastructure Layer - MySQL Customer Repository Implementation
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from interfaces.repositories.customer_repository import CustomerRepository
from domain.entities.customer import Customer
from infrastructure.models import CustomerModel

class MySQLCustomerRepository(CustomerRepository):
    """MySQL implementation of Customer repository using Django ORM"""
    
    def save(self, customer):
        """Save customer to database"""
        customer_model = CustomerModel(
            name=customer.name,
            email=customer.email,
            password=customer.password
        )
        customer_model.save()
        customer.id = customer_model.id
        return customer
    
    def find_by_id(self, customer_id):
        """Find customer by ID"""
        try:
            model = CustomerModel.objects.get(id=customer_id)
            return self._to_entity(model)
        except CustomerModel.DoesNotExist:
            return None
    
    def find_by_email(self, email):
        """Find customer by email"""
        try:
            model = CustomerModel.objects.get(email=email)
            return self._to_entity(model)
        except CustomerModel.DoesNotExist:
            return None
    
    def find_all(self):
        """Find all customers"""
        models = CustomerModel.objects.all()
        return [self._to_entity(model) for model in models]
    
    def _to_entity(self, model):
        """Convert Django model to domain entity"""
        return Customer(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password
        )
