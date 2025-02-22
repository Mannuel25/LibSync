import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

BASE_ADMIN_API = settings.ADMIN_API_URL


class EnrollUserAPIView(APIView):
    """Enroll users into the library"""

    def post(self, request):
        url = f"{BASE_ADMIN_API}/register/"
        response = requests.post(url, json=request.data)
        return Response(response.json(), status=response.status_code)


class ListAvailableBooksAPIView(APIView):
    """List all available books"""

    def get(self, request):
        url = f"{BASE_ADMIN_API}/books/"
        response = requests.get(url)
        return Response(response.json(), status=response.status_code)


class GetBookByIdAPIView(APIView):
    """Get a single book by ID"""

    def get(self, request, book_id):
        url = f"{BASE_ADMIN_API}/books/{book_id}/"
        response = requests.get(url)
        return Response(response.json(), status=response.status_code)


class FilterBooksAPIView(APIView):
    """Filter books by publisher or category"""

    def get(self, request):
        publisher = request.GET.get("publisher")
        category = request.GET.get("category")
        
        url = f"{BASE_ADMIN_API}/books/"
        params = {}
        if publisher:
            params["publisher"] = publisher
        if category:
            params["category"] = category
        
        response = requests.get(url, params=params)
        return Response(response.json(), status=response.status_code)


class BorrowBookAPIView(APIView):
    """Borrow a book by ID and specify duration in days"""

    def post(self, request):
        url = f"{BASE_ADMIN_API}/borrowed_books/"
        borrow_data = {
            "book": request.data.get("book"),
            "duration": request.data.get("duration"),
            "email": request.data.get("email")
        }
        response = requests.post(url, json=borrow_data)
        return Response(response.json(), status=response.status_code)
