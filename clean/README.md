# Clean Architecture Django - Book Store

## Architecture
Clean Architecture implementation with strict layer separation and dependency inversion.

## Project Structure
```
clean/
├── domain/                 # Enterprise business rules
│   └── entities/          # Customer, Book, Cart entities
├── usecases/              # Application business rules  
│   ├── customer_usecases.py
│   ├── book_usecases.py
│   └── cart_usecases.py
├── interfaces/            # Interface adapters
│   └── repositories/      # Repository interfaces
├── infrastructure/        # Frameworks & drivers
│   ├── database/          # MySQL repository implementations
│   └── models.py          # Django ORM models
└── framework/             # Django framework
    ├── bookstore/         # Django project
    ├── api/               # API views
    └── manage.py
```

## Clean Architecture Layers

### 1. Domain Layer (Innermost)
- Pure business entities
- No dependencies on external frameworks
- Contains validation and business logic

### 2. Use Cases Layer
- Application-specific business rules
- Orchestrates flow of data to/from entities
- Depends only on domain layer

### 3. Interface Adapters
- Abstract repository interfaces
- Defines contracts for data access
- Independent of specific implementations

### 4. Infrastructure Layer
- MySQL repository implementations using Django ORM
- Implements repository interfaces
- Depends on interfaces layer

### 5. Framework Layer (Outermost)
- Django web framework
- API views and routes
- Depends on all inner layers

## Dependency Rule
Source code dependencies point ONLY inward. Inner layers know nothing about outer layers.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database
Update `framework/bookstore/settings.py` with your MySQL credentials.

Lưu ý: dự án này mặc định dùng database **`bookstore_clean`** (đúng với các bảng `infrastructure_*`).

### 3. Create Database
```bash
mysql -u root -p < ../sql-scripts/create_clean_db.sql
```

### 4. Run Server
```bash
cd framework
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## Key Differences from Monolithic
- **Separation of Concerns**: Each layer has a single responsibility
- **Dependency Inversion**: Business logic doesn't depend on frameworks
- **Testability**: Domain and use cases can be tested without Django
- **Flexibility**: Easy to swap infrastructure (e.g., PostgreSQL instead of MySQL)
