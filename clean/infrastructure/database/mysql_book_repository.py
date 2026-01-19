# Infrastructure Layer - MySQL Book Repository Implementation
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from interfaces.repositories.book_repository import BookRepository
from domain.entities.book import Book
from infrastructure.models import BookModel
from django.db.models import Q

class MySQLBookRepository(BookRepository):
    """MySQL implementation of Book repository using Django ORM"""
    
    def save(self, book):
        """Save book to database"""
        book_model = BookModel(
            title=book.title,
            author=book.author,
            price=book.price,
            stock=book.stock
        )
        book_model.save()
        book.id = book_model.id
        return book
    
    def find_by_id(self, book_id):
        """Find book by ID"""
        try:
            model = BookModel.objects.get(id=book_id)
            return self._to_entity(model)
        except BookModel.DoesNotExist:
            return None
    
    def find_all(self):
        """Find all books"""
        models = BookModel.objects.all().order_by('title')
        return [self._to_entity(model) for model in models]
    
    def search(self, query):
        """Search books by title or author"""
        models = BookModel.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
        return [self._to_entity(model) for model in models]
    
    def _to_entity(self, model):
        """Convert Django model to domain entity"""
        return Book(
            id=model.id,
            title=model.title,
            author=model.author,
            price=float(model.price),
            stock=model.stock
        )
