
#📚 Library Management System API (Django REST Framework)
A backend API for managing library operations, built using Django and Django REST Framework (DRF). It handles everything from book inventory to issuing, returning, fine calculation, and user role management (Admin/Student).

**✅ Features**
**📘 Book Management**

 - Add Book
 - update Book
 - delete books

 - Search books by title, author, ISBN, or category

 - View book availability

**👥 User Management**

Student registration and login

Role-based access (Admin / Student)

**📦 Book Issue & Return**

Issue books to students with issue and due dates

Return books with fine calculation for late returns

**📊 Reports**

  - Generate daily, weekly, and monthly reports for:

  - Books issued

  - Books returned

  - Fines collected

**📌 Dashboards**

  - Student: view issued books, return dates, pending fines

  - Admin: view all transactions, total books, fine records

**🛠️ Tech Stack**
    - Pyhon
    - Django
    - Django REST Framework (DRF)
    - SQLite / MySQL (configurable)

**🚀 Getting Started**
Clone the repo:


    git clone https://github.com/yourusername/library-management-django.git
    cd library-management-django
**Install dependencies:**

    pip install -r requirements.txt
    Run migrations:

    python manage.py makemigrations
    python manage.py migrate
    Run server:
    
    python manage.py runserver
**🔑 Admin Login**
Use the Django admin panel at /admin/ for managing data directly.

**📬 API Testing**
You can use Postman or Swagger UI (if added) to test all API endpoints.

**📂 Folder Structure**

    library-management/
      ├── manage.py
      ├── lms/
      │   ├── settings.py
      │   └── urls.py
          └── library/
      ├── models.py
      ├── views.py
      ├── serializers.py
      └── urls.py    
