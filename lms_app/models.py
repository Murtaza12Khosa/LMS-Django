from django.db import models

# Create your models here.
#creating registration model

class Register(models.Model):
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book_Management(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    ISBN = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.title
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    
class IssuedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book_Management, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)