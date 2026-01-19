# Use Cases Layer - Book operations
from domain.entities.book import Book

class BookUseCases:
    """Use cases for book operations"""
    
    def __init__(self, book_repository):
        self.book_repository = book_repository
    
    def get_all_books(self):
        """Get all books"""
        return self.book_repository.find_all()
    
    def get_book_by_id(self, book_id):
        """Get book by ID"""
        return self.book_repository.find_by_id(book_id)
    
    def search_books(self, query):
        """Search books by title or author"""
        return self.book_repository.search(query)
