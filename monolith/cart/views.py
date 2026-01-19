from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, CartItem
from books.models import Book

def get_or_create_cart(request):
    """Get or create a cart for the logged-in customer"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return None
    
    cart, created = Cart.objects.get_or_create(customer_id=customer_id)
    return cart


def add_to_cart(request, book_id):
    # Check if customer is logged in
    if 'customer_id' not in request.session:
        messages.error(request, 'Please login to add items to cart')
        return redirect('login')
    
    cart = get_or_create_cart(request)
    book = get_object_or_404(Book, id=book_id)
    
    # Check stock
    if book.stock <= 0:
        messages.error(request, 'Sorry, this book is out of stock')
        return redirect('book_list')
    
    # Add or update cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book_id=book_id,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Updated quantity of "{book.title}" in your cart')
    else:
        messages.success(request, f'Added "{book.title}" to your cart')
    
    return redirect('book_list')


def view_cart(request):
    # Check if customer is logged in
    if 'customer_id' not in request.session:
        return redirect('login')
    
    cart = get_or_create_cart(request)
    cart_items = cart.items if cart else []
    
    # Calculate items with book details
    items_with_details = []
    for item in cart_items:
        items_with_details.append({
            'id': item.id,
            'book': item.book,
            'quantity': item.quantity,
            'subtotal': item.subtotal
        })
    
    total = cart.total_price if cart else 0
    
    return render(request, 'cart/view_cart.html', {
        'cart_items': items_with_details,
        'total': total
    })


def remove_from_cart(request, item_id):
    # Check if customer is logged in
    if 'customer_id' not in request.session:
        return redirect('login')
    
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    book_title = cart_item.book.title
    cart_item.delete()
    
    messages.success(request, f'Removed "{book_title}" from your cart')
    return redirect('view_cart')
