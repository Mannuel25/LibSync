from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

class FrontendAPITests(APITestCase):
    BASE_URL = "/frontend_api"

    @patch("requests.post")
    def test_enroll_user(self, mock_post):
        """Test enrolling a user."""
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"message": "User registered successfully"}
        response = self.client.post(f"{self.BASE_URL}/register/", {
            "email": "testuser@example.com",
            "password": "securepassword"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["message"], "User registered successfully")

    @patch("requests.get")
    def test_list_available_books(self, mock_get):
        """Test listing available books."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"id": 1, "title": "Test Book"}]
        response = self.client.get(f"{self.BASE_URL}/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["title"], "Test Book")

    @patch("requests.get")
    def test_get_book_by_id(self, mock_get):
        """Test retrieving a book by ID."""
        book_id = 1
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"id": book_id, "title": "Test Book"}
        response = self.client.get(f"{self.BASE_URL}/books/{book_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], "Test Book")

    @patch("requests.get")
    def test_filter_books(self, mock_get):
        """Test filtering books by publisher and category."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"id": 1, "title": "Filtered Book"}]
        response = self.client.get(f"{self.BASE_URL}/books/filter/?publisher=Test&category=Fiction")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]["title"], "Filtered Book")

    @patch("requests.post")
    def test_borrow_book(self, mock_post):
        """Test borrowing a book."""
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"message": "Book borrowed successfully"}
        response = self.client.post(f"{self.BASE_URL}/books/borrow/", {
            "book": 1,
            "duration": 7,
            "email": "testuser@example.com"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["message"], "Book borrowed successfully")

