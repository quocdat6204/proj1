# Interfaces Layer - Repository interfaces (abstract base classes)
from abc import ABC, abstractmethod

class CustomerRepository(ABC):
    """Abstract repository for Customer operations"""
    
    @abstractmethod
    def save(self, customer):
        """Save customer"""
        pass
    
    @abstractmethod
    def find_by_id(self, customer_id):
        """Find customer by ID"""
        pass
    
    @abstractmethod
    def find_by_email(self, email):
        """Find customer by email"""
        pass
    
    @abstractmethod
    def find_all(self):
        """Find all customers"""
        pass
