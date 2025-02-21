from django_filters import FilterSet
from .models import User, Book, BorrowedBook

class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class BookFilter(FilterSet):
    class Meta:
        model = Book
        exclude = ['summary']


class BorrowedBookFilter(FilterSet):
    class Meta:
        model = BorrowedBook
        fields = '__all__'