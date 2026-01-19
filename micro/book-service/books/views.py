from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

@api_view(['GET'])
def book_list(request):
    """Get all books"""
    books = Book.objects.all().order_by('title')
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def book_detail(request, book_id):
    """Get book by ID"""
    try:
        book = Book.objects.get(id=book_id)
        return Response(BookSerializer(book).data)
    except Book.DoesNotExist:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['PUT'])
def update_stock(request, book_id):
    """Update book stock"""
    try:
        book = Book.objects.get(id=book_id)
        quantity = request.data.get('quantity', 0)
        
        if book.stock < quantity:
            return Response(
                {'error': 'Not enough stock'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book.stock -= quantity
        book.save()
        return Response(BookSerializer(book).data)
    except Book.DoesNotExist:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )
