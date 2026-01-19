// API Configuration
const API_CONFIG = {
    CUSTOMER_SERVICE: 'http://localhost:8001',
    BOOK_SERVICE: 'http://localhost:8002',
    CART_SERVICE: 'http://localhost:8003'
};

// Application State
let currentUser = null;
let currentCart = null;
let books = [];

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadBooks();
    checkAuth();
});

// Authentication Functions
async function handleRegister(event) {
    event.preventDefault();
    const errorEl = document.getElementById('registerError');
    errorEl.textContent = '';

    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('registerConfirmPassword').value;

    if (password !== confirmPassword) {
        errorEl.textContent = 'Mật khẩu không khớp!';
        return;
    }

    try {
        const response = await fetch(`${API_CONFIG.CUSTOMER_SERVICE}/api/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name,
                email,
                password,
                confirm_password: confirmPassword
            })
        });

        const data = await response.json();

        if (response.ok) {
            currentUser = data;
            updateUI();
            closeModal('registerModal');
            alert('Đăng ký thành công!');
        } else {
            errorEl.textContent = data.error || data.password?.[0] || 'Đăng ký thất bại!';
        }
    } catch (error) {
        errorEl.textContent = 'Lỗi kết nối đến server!';
        console.error('Register error:', error);
    }
}

async function handleLogin(event) {
    event.preventDefault();
    const errorEl = document.getElementById('loginError');
    errorEl.textContent = '';

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch(`${API_CONFIG.CUSTOMER_SERVICE}/api/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            currentUser = data;
            updateUI();
            await loadCart();
            closeModal('loginModal');
            alert('Đăng nhập thành công!');
        } else {
            errorEl.textContent = data.error || 'Email hoặc mật khẩu không đúng!';
        }
    } catch (error) {
        errorEl.textContent = 'Lỗi kết nối đến server!';
        console.error('Login error:', error);
    }
}

function logout() {
    currentUser = null;
    currentCart = null;
    updateUI();
    hideCart();
    alert('Đã đăng xuất!');
}

function checkAuth() {
    // In a real app, you'd check localStorage or cookies
    // For now, we'll just update UI based on currentUser
    updateUI();
}

function updateUI() {
    const authButtons = document.getElementById('authButtons');
    const userInfo = document.getElementById('userInfo');
    const userName = document.getElementById('userName');

    if (currentUser) {
        authButtons.style.display = 'none';
        userInfo.style.display = 'flex';
        userName.textContent = currentUser.name;
    } else {
        authButtons.style.display = 'flex';
        userInfo.style.display = 'none';
    }

    // Re-render books so the "Add to cart" UI reflects current auth state.
    renderBooks();
}

// Modal Functions
function showLogin() {
    document.getElementById('loginModal').style.display = 'block';
}

function showRegister() {
    document.getElementById('registerModal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    // Clear form errors
    document.getElementById(modalId.replace('Modal', 'Error')).textContent = '';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

// Books Functions
async function loadBooks() {
    try {
        const response = await fetch(`${API_CONFIG.BOOK_SERVICE}/api/books/`);
        books = await response.json();
        renderBooks();
    } catch (error) {
        console.error('Error loading books:', error);
        document.getElementById('booksGrid').innerHTML = 
            '<div class="loading">Lỗi tải danh sách sách. Vui lòng kiểm tra kết nối.</div>';
    }
}

function renderBooks() {
    const grid = document.getElementById('booksGrid');
    
    if (books.length === 0) {
        grid.innerHTML = '<div class="loading">Không có sách nào.</div>';
        return;
    }

    grid.innerHTML = books.map(book => `
        <div class="book-card">
            <div class="book-title">${book.title}</div>
            <div class="book-author">Tác giả: ${book.author}</div>
            <div class="book-price">$${parseFloat(book.price).toFixed(2)}</div>
            <div class="book-stock ${book.stock === 0 ? 'out' : book.stock < 10 ? 'low' : ''}">
                ${book.stock === 0 ? 'Hết hàng' : book.stock < 10 ? `Còn ${book.stock} cuốn` : 'Còn hàng'}
            </div>
            ${currentUser ? `
                <div class="book-actions">
                    <input type="number" id="qty-${book.id}" min="1" max="${book.stock}" value="1" 
                           ${book.stock === 0 ? 'disabled' : ''}>
                    <button class="btn btn-primary" onclick="addToCart(${book.id})" 
                            ${book.stock === 0 ? 'disabled' : ''}>
                        Thêm vào giỏ
                    </button>
                </div>
            ` : '<p style="color: #666; font-size: 14px;">Vui lòng đăng nhập để mua sách</p>'}
        </div>
    `).join('');
}

async function addToCart(bookId) {
    if (!currentUser) {
        alert('Vui lòng đăng nhập để thêm sách vào giỏ!');
        showLogin();
        return;
    }

    const quantityInput = document.getElementById(`qty-${bookId}`);
    const quantity = parseInt(quantityInput.value) || 1;

    if (quantity < 1) {
        alert('Số lượng phải lớn hơn 0!');
        return;
    }

    try {
        // Get or create cart
        if (!currentCart || !currentCart.id) {
            console.log('Creating new cart for customer:', currentUser.id);
            const cartResponse = await fetch(`${API_CONFIG.CART_SERVICE}/api/carts/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ customer_id: currentUser.id })
            });

            if (!cartResponse.ok) {
                const errorData = await cartResponse.json().catch(() => ({}));
                throw new Error(errorData.error || `Lỗi tạo giỏ hàng: ${cartResponse.status}`);
            }

            const cartData = await cartResponse.json();
            console.log('Cart created:', cartData);
            currentCart = cartData;
        }

        // Ensure we have a valid cart ID
        if (!currentCart || !currentCart.id) {
            throw new Error('Không thể tạo giỏ hàng. Vui lòng thử lại.');
        }

        const cartId = currentCart.id;
        const addItemUrl = `${API_CONFIG.CART_SERVICE}/api/carts/${cartId}/items/`;
        console.log('Adding item to cart:', { cartId, bookId, quantity, url: addItemUrl });

        // Add item to cart
        const addResponse = await fetch(addItemUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                book_id: bookId,
                quantity: quantity
            })
        });

        console.log('Add item response status:', addResponse.status);

        if (addResponse.ok) {
            await loadCart();
            alert('Đã thêm vào giỏ hàng!');
        } else {
            const errorData = await addResponse.json().catch(() => ({}));
            console.error('Add item error:', errorData);
            const errorMsg = errorData.error || errorData.detail || `Lỗi ${addResponse.status}: Không thể thêm vào giỏ hàng!`;
            alert(errorMsg);
        }
    } catch (error) {
        console.error('Error adding to cart:', error);
        if (error.message) {
            alert(error.message);
        } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('Không thể kết nối đến server! Vui lòng kiểm tra:\n1. Cart Service có đang chạy trên port 8003?\n2. CORS đã được cấu hình đúng chưa?');
        } else {
            alert('Lỗi kết nối đến server! Chi tiết: ' + error.message);
        }
    }
}

// Cart Functions
async function loadCart() {
    if (!currentUser) {
        updateCartBadge(0);
        return;
    }

    try {
        // Get or create cart
        if (!currentCart) {
            const cartResponse = await fetch(`${API_CONFIG.CART_SERVICE}/api/carts/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ customer_id: currentUser.id })
            });
            const cartData = await cartResponse.json();
            currentCart = cartData;
        }

        // Get cart details
        const response = await fetch(`${API_CONFIG.CART_SERVICE}/api/carts/${currentCart.id}/`);
        const cartData = await response.json();
        
        currentCart = cartData;
        updateCartBadge(cartData.items ? cartData.items.length : 0);
        
        if (document.getElementById('cartSection').style.display !== 'none') {
            renderCart();
        }
    } catch (error) {
        console.error('Error loading cart:', error);
    }
}

function showCart() {
    if (!currentUser) {
        alert('Vui lòng đăng nhập để xem giỏ hàng!');
        showLogin();
        return;
    }

    document.getElementById('booksSection').style.display = 'none';
    document.getElementById('cartSection').style.display = 'block';
    renderCart();
}

function hideCart() {
    document.getElementById('cartSection').style.display = 'none';
    document.getElementById('booksSection').style.display = 'block';
}

function renderCart() {
    const cartContent = document.getElementById('cartContent');
    
    if (!currentCart || !currentCart.items || currentCart.items.length === 0) {
        cartContent.innerHTML = `
            <div class="empty-cart">
                <div class="empty-cart-icon">🛒</div>
                <h3>Giỏ hàng trống</h3>
                <p>Hãy thêm sách vào giỏ hàng của bạn!</p>
            </div>
        `;
        return;
    }

    let total = 0;
    const itemsHtml = currentCart.items.map(item => {
        const subtotal = parseFloat(item.subtotal || 0);
        total += subtotal;
        return `
            <div class="cart-item">
                <div class="cart-item-info">
                    <div class="cart-item-title">${item.book.title}</div>
                    <div class="cart-item-author">Tác giả: ${item.book.author}</div>
                    <div class="cart-item-details">
                        <span class="cart-item-price">$${parseFloat(item.book.price).toFixed(2)}</span>
                        <span class="cart-item-quantity">Số lượng: ${item.quantity}</span>
                        <span class="cart-item-subtotal">Tổng: $${subtotal.toFixed(2)}</span>
                    </div>
                </div>
                <div class="cart-item-actions">
                    <button class="btn btn-danger" onclick="removeFromCart(${item.item_id})">
                        Xóa
                    </button>
                </div>
            </div>
        `;
    }).join('');

    cartContent.innerHTML = itemsHtml + `
        <div class="cart-total">
            <div class="cart-total-label">Tổng cộng:</div>
            <div class="cart-total-amount">$${total.toFixed(2)}</div>
        </div>
    `;
}

async function removeFromCart(itemId) {
    if (!currentCart) return;

    try {
        const response = await fetch(
            `${API_CONFIG.CART_SERVICE}/api/carts/${currentCart.cart_id}/items/${itemId}/`,
            { method: 'DELETE' }
        );

        if (response.ok) {
            await loadCart();
            renderCart();
            alert('Đã xóa khỏi giỏ hàng!');
        } else {
            alert('Không thể xóa sản phẩm!');
        }
    } catch (error) {
        console.error('Error removing from cart:', error);
        alert('Lỗi kết nối đến server!');
    }
}

function updateCartBadge(count) {
    document.getElementById('cartBadge').textContent = count;
}
