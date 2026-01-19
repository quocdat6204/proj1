# Monolithic Django - Book Store

## Architecture
Traditional Django MVC (Model-View-Controller) architecture with all components in a single project.

## Project Structure
```
monolith/
├── bookstore/          # Main Django project
├── accounts/           # Customer authentication
├── books/              # Book catalog
├── cart/               # Shopping cart
├── templates/          # HTML templates
└── static/             # CSS, JS files
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database
Update `bookstore/settings.py` with your MySQL credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bookstore_monolith',
        'USER': 'root',
        'PASSWORD': 'your_password',  # Update this
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. Create Database
Run the SQL script to create the database and tables:
```bash
mysql -u root -p < ../sql-scripts/create_monolith_db.sql
```

### 4. Run Migrations (if needed)
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

### 5. Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## Features
- ✅ Customer registration and login
- ✅ View book catalog
- ✅ Add books to shopping cart
- ✅ View cart contents
- ✅ Remove items from cart

## Default Login
After running the SQL script, you can test the application by:
1. Registering a new account
2. Browsing the book catalog
3. Adding books to your cart
