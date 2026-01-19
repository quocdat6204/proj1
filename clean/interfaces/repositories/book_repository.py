# Interfaces Layer - Book repository interface
from abc import ABC, abstractmethod

class BookRepository(ABC):
    """Abstract repository for Book operations"""
    
    @abstractmethod
    def save(self, book):
        """Save book"""
        pass
    
    @abstractmethod
    def find_by_id(self, book_id):
        """Find book by ID"""
        pass
    
    @abstractmethod
    def find_all(self):
        """Find all books"""
        pass
    
    @abstractmethod
    def search(self, query):
        """Search books"""
        pass
