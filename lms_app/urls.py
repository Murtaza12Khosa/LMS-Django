from django.urls import path
from .views import register,login, add_category, add_book, delete_book,update_book, search_books, view_book_detail,issue_book,return_book,student_dashboard,admin_dashboard,generate_report

urlpatterns = [
    # Registration
    path('register/', register, name='register_user'),
    path('login/', login, name='login_user'), 
    path('add-category/', add_category, name="add_category"),
    path('add-book/', add_book, name='add_book'),
    path('delete-book/<int:book_id>/', delete_book, name="delete_book" ),
    path('update-book/<int:book_id>/', update_book, name="update_book"),
    path('search-books/', search_books, name='search_books'),
    path('view-book/<int:book_id>/', view_book_detail, name='view_book_detail'),
    path('issue-book/', issue_book, name='issue_book'),
    path('return-book/<int:issue_id>/', return_book, name='return_book'),
    path('student-dashboard/<int:student_id>/', student_dashboard, name='student_dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('reports/', generate_report, name='generate_report'),
]
