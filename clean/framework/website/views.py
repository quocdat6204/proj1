import os
import sys

from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404
from django.views.decorators.http import require_POST

# Đảm bảo có thể import được các layer bên trong (domain, usecases, infrastructure)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from usecases.book_usecases import BookUseCases
from usecases.cart_usecases import CartUseCases
from usecases.customer_usecases import CustomerUseCases
from infrastructure.database.mysql_book_repository import MySQLBookRepository
from infrastructure.database.mysql_cart_repository import MySQLCartRepository
from infrastructure.database.mysql_customer_repository import MySQLCustomerRepository


def _get_customer_id(request):
    return request.session.get("customer_id")


def _require_login(request):
    if "customer_id" not in request.session:
        messages.warning(request, "Bạn cần đăng nhập trước.")
        return False
    return True


def home(request):
    """Trang chủ: danh sách sách + ô tìm kiếm."""
    book_repo = MySQLBookRepository()
    book_usecases = BookUseCases(book_repo)

    q = request.GET.get("q", "").strip()
    if q:
        books = book_usecases.search_books(q)
    else:
        books = book_usecases.get_all_books()

    context = {
        "books": books,
        "query": q,
        "customer_id": _get_customer_id(request),
    }
    return render(request, "website/home.html", context)


def book_detail(request, book_id):
    """Chi tiết một cuốn sách."""
    book_repo = MySQLBookRepository()
    book_usecases = BookUseCases(book_repo)
    book = book_usecases.get_book_by_id(book_id)
    if not book:
        # Nếu không tìm thấy sách, trả về 404
        raise Http404("Book not found")

    return render(
        request,
        "website/book_detail.html",
        {"book": book, "customer_id": _get_customer_id(request)},
    )


def cart_view(request):
    """Xem giỏ hàng hiện tại."""
    if not _require_login(request):
        return redirect("website:login")

    customer_id = _get_customer_id(request)
    cart_repo = MySQLCartRepository()
    book_repo = MySQLBookRepository()
    cart_usecases = CartUseCases(cart_repo, book_repo)

    cart_data = cart_usecases.get_cart_contents(customer_id)
    return render(
        request,
        "website/cart.html",
        {
            "cart_data": cart_data,
            "customer_id": customer_id,
        },
    )


@require_POST
def add_to_cart(request, book_id):
    if not _require_login(request):
        return redirect("website:login")

    customer_id = _get_customer_id(request)
    quantity = int(request.POST.get("quantity", 1) or 1)

    cart_repo = MySQLCartRepository()
    book_repo = MySQLBookRepository()
    cart_usecases = CartUseCases(cart_repo, book_repo)

    try:
        cart_usecases.add_item_to_cart(customer_id, book_id, quantity)
        messages.success(request, "Đã thêm vào giỏ hàng.")
    except ValueError as e:
        messages.error(request, str(e))

    return redirect("website:cart")


@require_POST
def remove_from_cart(request, item_id):
    if not _require_login(request):
        return redirect("website:login")

    customer_id = _get_customer_id(request)
    cart_repo = MySQLCartRepository()
    book_repo = MySQLBookRepository()
    cart_usecases = CartUseCases(cart_repo, book_repo)

    try:
        cart_usecases.remove_item_from_cart(customer_id, item_id)
        messages.success(request, "Đã xóa khỏi giỏ hàng.")
    except ValueError as e:
        messages.error(request, str(e))

    return redirect("website:cart")


def register_view(request):
    """Đăng ký tài khoản khách hàng mới."""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        customer_repo = MySQLCustomerRepository()
        usecases = CustomerUseCases(customer_repo)

        try:
            customer = usecases.register_customer(name, email, password)
            request.session["customer_id"] = customer.id
            messages.success(request, "Đăng ký thành công.")
            return redirect("website:home")
        except ValueError as e:
            messages.error(request, str(e))

    return render(request, "website/register.html", {"customer_id": _get_customer_id(request)})


def login_view(request):
    """Đăng nhập."""
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        customer_repo = MySQLCustomerRepository()
        usecases = CustomerUseCases(customer_repo)

        try:
            customer = usecases.login_customer(email, password)
            request.session["customer_id"] = customer.id
            messages.success(request, "Đăng nhập thành công.")
            return redirect("website:home")
        except ValueError as e:
            messages.error(request, str(e))

    return render(request, "website/login.html", {"customer_id": _get_customer_id(request)})


def logout_view(request):
    request.session.pop("customer_id", None)
    messages.info(request, "Bạn đã đăng xuất.")
    return redirect("website:home")

