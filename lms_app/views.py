from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Register, Category, Book_Management, IssuedBook, Student
from .serializers import RegisterSerializer, CategorySerializer, Book_ManagementSerializer, IssuedBookSerializer,IssuedBookDashboardSerializer
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Count
from django.utils.timezone import now, timedelta

@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Register.objects.get(email=email, password=password)
        return Response({
            "message": "Login successful",
            "email": user.email,
            "role": user.role
        }, status=status.HTTP_200_OK)
    except Register.DoesNotExist:
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
# 🔹 Add Category
@api_view(["POST"])
def add_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🔹 Add Book
@api_view(["POST"])
def add_book(request):
    try:
        category_name = request.data.get('category')
        category = Category.objects.get(name=category_name)

        book_data = {
            "title": request.data.get('title'),
            "author": request.data.get('author'),
            "ISBN": request.data.get('ISBN'),
            "category": category.id,
            "quantity": request.data.get('quantity'),
        }

        serializer =Book_ManagementSerializer(data=book_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Category.DoesNotExist:
        return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["DELETE"])
def delete_book(request, book_id):
    try:
        book = Book_Management.objects.get(id=book_id)
        book.delete()
        return Response({"message": "Book deleted successfully"}, status=status.HTTP_200_OK)
    except Book_Management.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(["PUT"])
def update_book(request, book_id):
    try:
        book = Book_Management.objects.get(id=book_id)

        category_name = request.data.get('category')
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        updated_data = {
            "title": request.data.get("title", book.title),
            "author": request.data.get("author", book.author),
            "ISBN": request.data.get("ISBN", book.ISBN),
            "category": category.id,
            "quantity": request.data.get("quantity", book.quantity)
        }

        serializer = Book_ManagementSerializer(book, data=updated_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Book updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Book_Management.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(["GET"])
def search_books(request):
    query = request.GET.get('q', '')

    books = Book_Management.objects.filter(
        Q(title__icontains=query) |
        Q(author__icontains=query) |
        Q(ISBN__icontains=query) |
        Q(category__name__icontains=query)
    ).distinct()

    serializer = Book_ManagementSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(["GET"])
def view_book_detail(request, book_id):
    try:
        book = Book_Management.objects.get(id=book_id)
        serializer = Book_ManagementSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Book_Management.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
@api_view(['POST'])
def issue_book(request):
    try:
        student_id = request.data.get("student_id")
        book_id = request.data.get("book_id")

        book = Book_Management.objects.get(id=book_id)
        student = Student.objects.get(id=student_id)

        if book.quantity <= 0:
            return Response({"error": "Book not available"}, status=status.HTTP_400_BAD_REQUEST)

        due_date = timezone.now().date() + timedelta(days=7)  # 7-day loan

        issued_book = IssuedBook.objects.create(
            student=student,
            book=book,
            due_date=due_date
        )

        book.quantity -= 1
        book.save()

        serializer = IssuedBookSerializer(issued_book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Book_Management.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
def return_book(request, issue_id):
    try:
        issued = IssuedBook.objects.get(id=issue_id)

        if issued.return_date:
            return Response({"message": "Book already returned"}, status=status.HTTP_400_BAD_REQUEST)

        return_date = timezone.now().date()
        issued.return_date = return_date

        # Fine: Rs.10 per day late
        if return_date > issued.due_date:
            days_late = (return_date - issued.due_date).days
            issued.fine = days_late * 10
        else:
            issued.fine = 0

        issued.save()

        # Increase book quantity
        book = issued.book
        book.quantity += 1
        book.save()

        serializer = IssuedBookSerializer(issued)
        return Response({
            "message": "Book returned successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    except IssuedBook.DoesNotExist:
        return Response({"error": "Issued book record not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['GET'])
def student_dashboard(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        issued_books = IssuedBook.objects.filter(student=student)

        serializer = IssuedBookDashboardSerializer(issued_books, many=True)
        return Response({
            "student_name": student.name,
            "issued_books": serializer.data
        }, status=status.HTTP_200_OK)

    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
    
                    ###ADMIN Dashboard
@api_view(['GET'])
def admin_dashboard(request):
    try:
        total_books = Book_Management.objects.aggregate(total=Count('id'))['total']
        total_issued = IssuedBook.objects.count()
        total_fine = IssuedBook.objects.aggregate(total=Sum('fine'))['total'] or 0.00

        issued_books = IssuedBook.objects.select_related('book', 'student').all()

        data = []
        for issue in issued_books:
            data.append({
                'book_title': issue.book.title,
                'student_name': issue.student.name,
                'issue_date': issue.issue_date,
                'due_date': issue.due_date,
                'return_date': issue.return_date,
                'fine': str(issue.fine),
            })

        return Response({
            "total_books": total_books,
            "total_issued_books": total_issued,
            "total_fine_collected": str(total_fine),
            "issued_book_details": data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['GET'])
def generate_report(request):
    range_type = request.GET.get('range', 'daily')

    try:
        today = now().date()
        if range_type == 'daily':
            start_date = today
        elif range_type == 'weekly':
            start_date = today - timedelta(days=7)
        elif range_type == 'monthly':
            start_date = today - timedelta(days=30)
        else:
            return Response({"error": "Invalid range. Use daily, weekly, or monthly."}, status=400)

        end_date = today

        # Issued books count
        issued_count = IssuedBook.objects.filter(issue_date__range=[start_date, end_date]).count()

        # Returned books count
        returned_count = IssuedBook.objects.filter(return_date__range=[start_date, end_date]).count()

        # Fine collected
        fine_total = IssuedBook.objects.filter(return_date__range=[start_date, end_date]).aggregate(total=Sum('fine'))['total'] or 0.00

        return Response({
            "range": range_type,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "books_issued": issued_count,
            "books_returned": returned_count,
            "fine_collected": str(fine_total)
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=500)