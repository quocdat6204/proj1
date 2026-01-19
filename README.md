# Book Store Web System - Software Architecture Assignment

## Project Overview
This project implements a Book Store Web System in three different architectural styles:
1. **Monolithic Architecture** - Traditional Django MVC
2. **Clean Architecture** - Layered architecture with dependency inversion
3. **Microservices Architecture** - Distributed services with REST APIs

## Directory Structure
```
assign1/
├── monolith/          # Monolithic Django implementation
├── clean/             # Clean Architecture implementation
├── micro/             # Microservices implementation
│   ├── customer-service/
│   ├── book-service/
│   └── cart-service/
├── sql-scripts/       # Database creation scripts
├── uml-diagrams/      # UML design files
└── docs/              # Documentation
```

## Technologies Used
- **Backend**: Django 4.2+, Django REST Framework
- **Database**: MySQL 8.0+
- **Language**: Python 3.8+
- **API**: REST APIs for microservices

## Entities
All versions implement the following entities:
- **Customer**: id, name, email, password
- **Book**: id, title, author, price, stock
- **Cart**: id, customer_id, created_at
- **CartItem**: id, cart_id, book_id, quantity

## Functional Requirements
✅ Customer registration and login  
✅ View book catalog  
✅ Add books to shopping cart  
✅ View shopping cart contents

## Quick Start

### Prerequisites
```bash
pip install Django>=4.2
pip install mysqlclient
pip install djangorestframework
```

### Database Setup
```bash
# Create all databases
mysql -u root -p < sql-scripts/create_monolith_db.sql
mysql -u root -p < sql-scripts/create_clean_db.sql
mysql -u root -p < sql-scripts/create_micro_customer_db.sql
mysql -u root -p < sql-scripts/create_micro_book_db.sql
mysql -u root -p < sql-scripts/create_micro_cart_db.sql
```

### Run Monolithic Version
```bash
cd monolith
pip install -r requirements.txt
python manage.py runserver
# Visit http://localhost:8000
```

### Run Clean Architecture Version
```bash
cd clean/framework
pip install -r ../requirements.txt
python manage.py runserver
# Visit http://localhost:8000
```

### Run Microservices Version
```bash
# Terminal 1
cd micro/customer-service
python manage.py runserver 8001

# Terminal 2
cd micro/book-service
python manage.py runserver 8002

# Terminal 3
cd micro/cart-service
python manage.py runserver 8003
```

## Architecture Comparison

| Aspect | Monolithic | Clean Architecture | Microservices |
|--------|-----------|-------------------|---------------|
| **Deployment** | Single unit | Single unit | Independent services |
| **Database** | Single shared | Single shared | Database per service |
| **Scalability** | Vertical only | Vertical only | Horizontal per service |
| **Complexity** | Low | Medium | High |
| **Team Structure** | Single team | Single team | Multiple teams |
| **Technology** | Unified stack | Unified stack | Polyglot possible |
| **Fault Isolation** | Low | Low | High |
| **Testing** | Integration tests | Unit + Integration | Service + Integration |

## UML Diagrams
See `uml-diagrams/README.md` for:
- Class Diagram
- MVC Layer Diagram (Monolithic)
- Clean Architecture Diagram
- Microservices Architecture Diagram

All diagrams are created with Mermaid and can be imported into Visual Paradigm.

## Documentation
- `/monolith/README.md` - Monolithic architecture details
- `/clean/README.md` - Clean architecture principles
- `/micro/README.md` - Microservices setup and API documentation
- `/uml-diagrams/README.md` - UML design documentation

## Author
Software Architecture and Design Assignment
