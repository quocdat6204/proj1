from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
import requests

BOOK_SERVICE_URL = 'http://localhost:8002'

@api_view(['POST'])
def create_cart(request):
    """Create a new cart"""
    customer_id = request.data.get('customer_id')
    if not customer_id:
        return Response(
            {'error': 'customer_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    cart, created = Cart.objects.get_or_create(customer_id=customer_id)
    return Response(
        CartSerializer(cart).data,
        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
    )


@api_view(['GET'])
def get_cart(request, cart_id):
    """Get cart with items and book details"""
    try:
        cart = Cart.objects.get(id=cart_id)
        cart_data = CartSerializer(cart).data
        
        # Fetch book details for each item
        items_with_books = []
        total = 0
        
        for item in cart.items.all():
            try:
                response = requests.get(f'{BOOK_SERVICE_URL}/api/books/{item.book_id}/')
                if response.status_code == 200:
                    book_data = response.json()
                    subtotal = float(book_data['price']) * item.quantity
                    items_with_books.append({
                        'item_id': item.id,
                        'book': book_data,
                        'quantity': item.quantity,
                        'subtotal': subtotal
                    })
                    total += subtotal
            except:
                pass
        
        return Response({
            'cart_id': cart.id,
            'customer_id': cart.customer_id,
            'items': items_with_books,
            'total': total
        })
    except Cart.DoesNotExist:
        return Response(
            {'error': 'Cart not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
def add_item(request, cart_id):
    """Add item to cart"""
    try:
        cart = Cart.objects.get(id=cart_id)
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity', 1)
        
        # Check book availability via book service
        try:
            response = requests.get(f'{BOOK_SERVICE_URL}/api/books/{book_id}/')
            if response.status_code != 200:
                return Response(
                    {'error': 'Book not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            book_data = response.json()
            if book_data['stock'] < quantity:
                return Response(
                    {'error': 'Not enough stock'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'Could not verify book availability'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book_id=book_id,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
    except Cart.DoesNotExist:
        return Response(
            {'error': 'Cart not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
def remove_item(request, cart_id, item_id):
    """Remove item from cart"""
    try:
        cart = Cart.objects.get(id=cart_id)
        item = CartItem.objects.get(id=item_id, cart=cart)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return Response(
            {'error': 'Cart or item not found'},
            status=status.HTTP_404_NOT_FOUND
        )
