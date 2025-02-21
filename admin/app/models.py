from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from datetime import timedelta, date
from .manager import UserProfileManager


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True, db_index=True)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # returns the full name of the user
        return f"{self.first_name.title()} {self.last_name.title()}"


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    summary = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # calculate return date based on borrow_date and loan duration when BorrowedBook instance is created
        if not self.pk:
            self.return_date = self.borrow_date + timedelta(days=7)  # Default to 7 days; can be configurable
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    @property
    def is_overdue(self):
        return self.return_date < date.today() and not self.returned

