# Use Cases Layer - Cart operations
from domain.entities.cart import Cart, CartItem

class CartUseCases:
    """Use cases for cart operations"""
    
    def __init__(self, cart_repository, book_repository):
        self.cart_repository = cart_repository
        self.book_repository = book_repository
    
    def get_or_create_cart(self, customer_id):
        """Get or create cart for customer"""
        cart = self.cart_repository.find_by_customer_id(customer_id)
        if not cart:
            cart = Cart(customer_id=customer_id)
            cart = self.cart_repository.save(cart)
        return cart
    
    def add_item_to_cart(self, customer_id, book_id, quantity=1):
        """Add item to cart"""
        # Get or create cart
        cart = self.get_or_create_cart(customer_id)
        
        # Validate book exists and has stock
        book = self.book_repository.find_by_id(book_id)
        if not book:
            raise ValueError("Book not found")
        if not book.is_available():
            raise ValueError("Book is out of stock")
        
        # Add item
        cart_item = CartItem(cart_id=cart.id, book_id=book_id, quantity=quantity)
        cart_item.validate()
        
        return self.cart_repository.add_item(cart.id, cart_item)
    
    def get_cart_contents(self, customer_id):
        """Get cart contents with book details"""
        cart = self.cart_repository.find_by_customer_id(customer_id)
        if not cart:
            return {'items': [], 'total': 0}
        
        # Get items with book details
        items_with_books = []
        book_prices = {}
        
        for item in cart.items:
            book = self.book_repository.find_by_id(item.book_id)
            if book:
                items_with_books.append({
                    'item': item,
                    'book': book,
                    'subtotal': item.calculate_subtotal(book.price)
                })
                book_prices[book.id] = book.price
        
        total = cart.calculate_total(book_prices)
        
        return {
            'cart': cart,
            'items': items_with_books,
            'total': total
        }
    
    def remove_item_from_cart(self, customer_id, item_id):
        """Remove item from cart"""
        cart = self.cart_repository.find_by_customer_id(customer_id)
        if not cart:
            raise ValueError("Cart not found")
        
        return self.cart_repository.remove_item(cart.id, item_id)
