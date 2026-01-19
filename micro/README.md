# Microservices Django - Book Store

## Architecture
Microservices architecture with independent services communicating via REST APIs.

## Services

### 1. Customer Service (Port 8001)
**Database:** `bookstore_customer`  
**Endpoints:**
- `POST /api/register/` - Register new customer
- `POST /api/login/` - Customer login
- `GET /api/customers/{id}/` - Get customer details

### 2. Book Service (Port 8002)
**Database:** `bookstore_book`  
**Endpoints:**
- `GET /api/books/` - List all books
- `GET /api/books/{id}/` - Get book details
- `PUT /api/books/{id}/stock/` - Update book stock

### 3. Cart Service (Port 8003)
**Database:** `bookstore_cart`  
**Endpoints:**
- `POST /api/carts/` - Create cart
- `GET /api/carts/{id}/` - Get cart with items
- `POST /api/carts/{id}/items/` - Add item to cart
- `DELETE /api/carts/{id}/items/{item_id}/` - Remove item

## Inter-Service Communication
- Cart Service → Book Service: Verify book availability and fetch book details
- Services communicate via HTTP REST APIs

## Setup Instructions

### 1. Create Databases
```bash
mysql -u root -p < ../../sql-scripts/create_micro_customer_db.sql
mysql -u root -p < ../../sql-scripts/create_micro_book_db.sql
mysql -u root -p < ../../sql-scripts/create_micro_cart_db.sql
```

### 2. Configure Each Service
Update database settings in each service's `settings.py`:
- Customer Service: `customer_service/settings.py` → `bookstore_customer`
- Book Service: `book_service/settings.py` → `bookstore_book`
- Cart Service: `cart_service/settings.py` → `bookstore_cart`

### 3. Install Dependencies
```bash
cd customer-service && pip install -r requirements.txt
cd ../book-service && pip install -r requirements.txt
cd ../cart-service && pip install -r requirements.txt
```

### 4. Run Services (in separate terminals)
```bash
# Terminal 1 - Customer Service
cd customer-service
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py runserver 8001

# Terminal 2 - Book Service
cd book-service
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py runserver 8002

# Terminal 3 - Cart Service
cd cart-service
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py runserver 8003
```

## API Testing Examples

### Register Customer
```bash
curl -X POST http://localhost:8001/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"password123","confirm_password":"password123"}'
```

### Get Books
```bash
curl http://localhost:8002/api/books/
```

### Create Cart and Add Item
```bash
# Create cart
curl -X POST http://localhost:8003/api/carts/ \
  -H "Content-Type: application/json" \
  -d '{"customer_id":1}'

# Add book to cart
curl -X POST http://localhost:8003/api/carts/1/items/ \
  -H "Content-Type: application/json" \
  -d '{"book_id":1,"quantity":2}'
```

## Frontend Interface

Một giao diện web đầy đủ đã được tạo trong thư mục `frontend/` với các tính năng:

- **Đăng ký/Đăng nhập**: Quản lý tài khoản khách hàng
- **Xem sách**: Duyệt danh sách tất cả sách có sẵn
- **Giỏ hàng**: Thêm, xem và xóa sách khỏi giỏ hàng
- **Tính tổng tiền**: Tự động tính tổng giá trị đơn hàng

### Chạy Frontend

```bash
cd frontend
python -m http.server 8000
```

Sau đó truy cập: `http://localhost:8000`

Xem thêm hướng dẫn chi tiết trong `frontend/README.md`

## Key Advantages
- **Independence**: Each service can be deployed and scaled independently
- **Technology Diversity**: Services can use different tech stacks
- **Fault Isolation**: Failure in one service doesn't crash the entire system
- **Team Autonomy**: Different teams can work on different services
