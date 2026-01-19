from django.shortcuts import render
from .models import Book

def book_list(request):
    # Check if customer is logged in
    if 'customer_id' not in request.session:
        from django.shortcuts import redirect
        return redirect('login')
    
    books = Book.objects.all().order_by('title')
    return render(request, 'books/book_list.html', {'books': books})


def book_detail(request, pk):
    # Check if customer is logged in
    if 'customer_id' not in request.session:
        from django.shortcuts import redirect
        return redirect('login')
    
    book = Book.objects.get(pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})
