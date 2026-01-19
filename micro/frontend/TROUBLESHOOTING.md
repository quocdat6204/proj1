# Hướng dẫn xử lý lỗi kết nối

## Kiểm tra các services có đang chạy

### 1. Kiểm tra Customer Service (port 8001)
Mở trình duyệt hoặc dùng curl:
```
http://localhost:8001/api/register/
```
Hoặc:
```bash
curl http://localhost:8001/api/register/
```

### 2. Kiểm tra Book Service (port 8002)
```
http://localhost:8002/api/books/
```
Hoặc:
```bash
curl http://localhost:8002/api/books/
```

### 3. Kiểm tra Cart Service (port 8003)
```
http://localhost:8003/api/carts/
```
Hoặc:
```bash
curl http://localhost:8003/api/carts/
```

## Các lỗi thường gặp

### Lỗi "Lỗi kết nối đến server!"
**Nguyên nhân:**
- Service chưa được khởi động
- Port bị conflict
- Firewall chặn kết nối

**Giải pháp:**
1. Kiểm tra các services có đang chạy:
   ```powershell
   # Terminal 1
   cd customer-service
   python manage.py runserver 8001

   # Terminal 2
   cd book-service
   python manage.py runserver 8002

   # Terminal 3
   cd cart-service
   python manage.py runserver 8003
   ```

2. Kiểm tra CORS đã được cấu hình trong settings.py của mỗi service

3. Mở Developer Tools (F12) trong trình duyệt và xem tab Console để xem lỗi chi tiết

### Lỗi CORS
Nếu thấy lỗi về CORS trong console:
- Đảm bảo `django-cors-headers` đã được cài đặt
- Kiểm tra `CORS_ALLOWED_ORIGINS` trong settings.py có chứa URL của frontend

### Lỗi Database
Nếu thấy lỗi về database:
- Kiểm tra MySQL đã được cài đặt và đang chạy
- Kiểm tra các database đã được tạo (bookstore_book, bookstore_customer, bookstore_cart)
- Kiểm tra thông tin đăng nhập MySQL trong settings.py (USER, PASSWORD)
