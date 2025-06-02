from rest_framework import serializers
from .models import Register, Category, Book_Management, IssuedBook

class RegisterSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Register
        fields = "__all__"  
#category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
#Book_Management Serializer
class Book_ManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book_Management
        fields = ['id', 'title', 'author', 'ISBN', 'category', 'quantity']
class IssuedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuedBook
        fields = '__all__'

class IssuedBookDashboardSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = IssuedBook
        fields = ['book_title', 'issue_date', 'due_date', 'return_date', 'fine']