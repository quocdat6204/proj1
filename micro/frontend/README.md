# Frontend - Bookstore Web Interface

Giao diện web cho hệ thống Bookstore Microservices.

## Cách sử dụng

### 1. Mở giao diện

Có thể mở file `index.html` trực tiếp trong trình duyệt hoặc sử dụng một web server đơn giản:

**Sử dụng Python:**
```bash
cd frontend
python -m http.server 8000
```

**Sử dụng Node.js (http-server):**
```bash
cd frontend
npx http-server -p 8000
```

Sau đó truy cập: `http://localhost:8000`

### 2. Đảm bảo các microservices đang chạy

- Customer Service: `http://localhost:8001`
- Book Service: `http://localhost:8002`
- Cart Service: `http://localhost:8003`

### 3. Tính năng

- **Đăng ký/Đăng nhập**: Tạo tài khoản mới hoặc đăng nhập vào hệ thống
- **Xem sách**: Duyệt danh sách tất cả sách có sẵn
- **Thêm vào giỏ hàng**: Thêm sách vào giỏ hàng với số lượng mong muốn
- **Quản lý giỏ hàng**: Xem, xóa các sản phẩm trong giỏ hàng
- **Tính tổng tiền**: Tự động tính tổng giá trị đơn hàng

### 4. Cấu trúc file

- `index.html`: Cấu trúc HTML chính
- `styles.css`: Styling và layout
- `app.js`: Logic xử lý và kết nối API

### 5. Lưu ý

- Giao diện yêu cầu các microservices phải đã được cấu hình CORS
- Đảm bảo MySQL đã được cấu hình và các database đã được tạo
- Các API endpoints phải khớp với cấu hình trong `app.js`
