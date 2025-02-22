from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view as gs
from drf_yasg import openapi
from rest_framework import permissions
from .views import *


schema_view = gs(
    openapi.Info(
        title="LibSync Frontend API",
        default_version='1.0.0',
        description="Documentation for LibSync Frontend API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="oluwasegunprosperity@gmail.com@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('frontend_api/register/', EnrollUserAPIView.as_view(), name='register'),
    path('frontend_api/books/', ListAvailableBooksAPIView.as_view(), name='available_books'),
    path('frontend_api/books/<int:book_id>/', GetBookByIdAPIView.as_view(), name='get-book-by-id'),
    path('frontend_api/books/filter/', FilterBooksAPIView.as_view(), name='filter-books'),
    path('frontend_api/books/borrow/', BorrowBookAPIView.as_view(), name='borrow-book'),
]
