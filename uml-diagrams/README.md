# Book Store Web System - UML Diagrams

## 1. Class Diagram

```mermaid
classDiagram
    class Customer {
        +int id
        +string name
        +string email
        +string password
        +datetime created_at
        +validate() bool
    }
    
    class Book {
        +int id
        +string title
        +string author
        +decimal price
        +int stock
        +datetime created_at
        +isAvailable() bool
        +reduceStock(quantity)
    }
    
    class Cart {
        +int id
        +int customer_id
        +datetime created_at
        +calculateTotal() decimal
    }
    
    class CartItem {
        +int id
        +int cart_id
        +int book_id
        +int quantity
        +datetime created_at
        +calculateSubtotal() decimal
    }
    
    Customer "1" --> "0..1" Cart : has
    Cart "1" --> "*" CartItem : contains
    Book "1" --> "*" CartItem : referenced by
```

## 2. Monolithic MVC Layer Diagram

```mermaid
graph TB
    subgraph "Presentation Layer"
        V[Views/Templates]
        U[URLs]
    end
    
    subgraph "Business Logic Layer"
        AC[Accounts Controller]
        BC[Books Controller]
        CC[Cart Controller]
    end
    
    subgraph "Data Access Layer"
        CM[Customer Model]
        BM[Book Model]
        CAM[Cart Model]
        CIM[CartItem Model]
    end
    
    subgraph "Database"
        DB[(MySQL - bookstore_monolith)]
    end
    
    V --> AC
    V --> BC
    V --> CC
    
    AC --> CM
    BC --> BM
    CC --> CAM
    CC --> CIM
    
    CM --> DB
    BM --> DB
    CAM --> DB
    CIM --> DB
```

## 3. Clean Architecture Diagram

```mermaid
graph TB
    subgraph "Framework Layer (Outermost)"
        Django[Django Web Framework]
        API[REST API Views]
        Templates[Templates]
    end
    
    subgraph "Infrastructure Layer"
        MySQLRepo["MySQL Repositories<br/>(Django ORM)"]
        Models[Django Models]
    end
    
    subgraph "Interface Adapters"
        RepoInterface["Repository Interfaces<br/>(Abstract Classes)"]
    end
    
    subgraph "Use Cases Layer"
        CU[Customer Use Cases]
        BU[Book Use Cases]
        CAU[Cart Use Cases]
    end
    
    subgraph "Domain Layer (Innermost)"
        CE[Customer Entity]
        BE[Book Entity]
        CAE[Cart Entity]
        CIE[CartItem Entity]
    end
    
    Django --> MySQLRepo
    API --> CU
    API --> BU
    API --> CAU
    
    MySQLRepo --> RepoInterface
    RepoInterface --> CU
    RepoInterface --> BU
    RepoInterface --> CAU
    
    CU --> CE
    BU --> BE
    CAU --> CAE
    CAU --> CIE
    
    Models --> Database[(MySQL)]
    
    style CE fill:#667eea
    style BE fill:#667eea
    style CAE fill:#667eea
    style CIE fill:#667eea
```

## 4. Microservices Architecture Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        Client[Web/Mobile Client]
    end
    
    subgraph "Service Layer"
        CS["Customer Service<br/>:8001"]
        BS["Book Service<br/>:8002"]
        CAS["Cart Service<br/>:8003"]
    end
    
    subgraph "Data Layer"
        CDB[(Customer DB)]
        BDB[(Book DB)]
        CADB[(Cart DB)]
    end
    
    Client -->|Register/Login| CS
    Client -->|Browse Books| BS
    Client -->|Manage Cart| CAS
    
    CAS -->|Verify Book| BS
    
    CS --> CDB
    BS --> BDB
    CAS --> CADB
    
    style CS fill:#f9a825
    style BS fill:#66bb6a
    style CAS fill:#42a5f5
```

## Diagram Descriptions

### Class Diagram
Shows the domain entities and their relationships:
- **Customer** has one **Cart**
- **Cart** contains multiple **CartItem**s
- Each **CartItem** references a **Book**

### MVC Layer Diagram (Monolithic)
Three-tier architecture:
- **Presentation**: Views and URL routing
- **Business Logic**: Controllers handling business rules
- **Data Access**: Models interacting with single database

### Clean Architecture Diagram
Concentric circles showing dependency rule:
- **Domain** (center): Pure business entities
- **Use Cases**: Application business rules
- **Interfaces**: Abstract repository contracts
- **Infrastructure**: Framework-specific implementations
- **Framework** (outer): Django web framework

Dependencies point inward only!

### Microservices Architecture Diagram
Distributed system with three independent services:
- Each service has its own database (database per service pattern)
- Services communicate via REST APIs
- Cart service depends on Book service for validation
- Horizontal scalability and fault isolation

## Visual Paradigm Import

To import these diagrams into Visual Paradigm:
1. Open Visual Paradigm
2. Create New Project
3. Use "Reverse Engineering" → "Mermaid" to import above diagrams
4. Or manually recreate using the structure shown above

## Export Formats
These diagrams can be exported as:
- PNG images
- PDF documents
- SVG vectors
