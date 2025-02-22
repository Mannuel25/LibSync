from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Book, BorrowedBook
from django.utils.timezone import now

User = get_user_model()

class APITests(APITestCase):
    """Test cases for authentication, books, and borrowing books."""

    def setUp(self):
        """Setup common data for the tests."""
        self.user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password": "SecurePassword123!"
        }
        self.user = User.objects.create_user(**self.user_data)

        self.book_data = {
            "title": "Sample Book",
            "author": "Author Name",
            "publisher": "Publisher Name",
            "category": "Fiction",
            "isbn": "1234567890123",
            "summary": "This is a sample book summary."
        }
        self.book = Book.objects.create(**self.book_data)
        self.book_id = self.book.id

        self.borrowed_book = BorrowedBook.objects.create(user=self.user, book=self.book, borrow_date=now().date())

        # Generate tokens
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    #  Authentication Tests 
    # def test_user_signup(self):
    #     """Test user registration."""
    #     response = self.client.post('/admin_api/register/', {
    #         "first_name": "Jane",
    #         "last_name": "Doe",
    #         "email": "janedoe@example.com",
    #         "password": "StrongPass123!"
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_user_login(self):
    #     """Test user login."""
    #     response = self.client.post('/admin_api/login/', {
    #         "email": self.user_data["email"],
    #         "password": self.user_data["password"]
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_token_refresh(self):
    #     """Test refreshing access token."""
    #     refresh = RefreshToken.for_user(self.user)
    #     response = self.client.post('/admin_api/token/refresh/', {
    #         "refresh_token": str(refresh)
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #  Book Tests 
    # def test_list_books(self):
    #     """Test retrieving a list of books."""
    #     response = self.client.get('/admin_api/books/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_create_book(self):
    #     """Test creating a new book."""
    #     response = self.client.post('/admin_api/books/', {
    #         "title": "New Book",
    #         "author": "New Author",
    #         "isbn": "9876543210987",
    #         "publisher": "New Publisher",
    #         "category": "New Category",
    #         "summary": "This is a new book summary."
    #     }, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_get_book(self):
    #     """Test retrieving a single book."""
    #     response = self.client.get(f'/admin_api/books/{self.book_id}/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_book_patch(self):
    #     """Test partially updating a book."""
    #     response = self.client.patch(f'/admin_api/books/{self.book_id}/', {
    #         "title": "Updated Book Title"
    #     }, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_book_put(self):
    #     """Test fully updating a book."""
    #     response = self.client.put(f'/admin_api/books/{self.book_id}/', {
    #         "title": "Updated Book",
    #         "author": "Updated Author",
    #         "isbn": "1111222233334",
    #         "publisher": "Updated Publisher",
    #         "category": "Updated Category",
    #         "summary": "This is a new book summary."
    #     }, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_delete_book(self):
    #     """Test deleting a book."""
    #     response = self.client.delete(f'/admin_api/books/{self.book_id}/')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #  Borrowed Book Tests 
    def test_list_borrowed_books(self):
        """Test retrieving a list of borrowed books."""
        response = self.client.get('/admin_api/borrowed_books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_borrow_book(self):
        """Test borrowing a book."""
        response = self.client.post('/admin_api/borrowed_books/', {
            "email": self.user.email,
            "book": self.book.id,
            "duration": 7
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_borrowed_book(self):
        """Test retrieving a borrowed book's details."""
        response = self.client.get(f'/admin_api/borrowed_books/{self.borrowed_book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_borrowed_book_patch(self):
        """Test partially updating a borrowed book (e.g., marking as returned)."""
        response = self.client.patch(f'/admin_api/borrowed_books/{self.borrowed_book.id}/', {
            "returned": True,
            "return_date": now().date()
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_borrowed_book_put(self):
        """Test fully updating a borrowed book."""
        response = self.client.put(f'/admin_api/borrowed_books/{self.borrowed_book.id}/', {
            "user": self.user.id,
            "book": self.book.id,
            "returned": True,
            "duration": 7
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_borrowed_book(self):
        """Test deleting a borrowed book record."""
        response = self.client.delete(f'/admin_api/borrowed_books/{self.borrowed_book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

