from requests import Response
from .models import *
from .filters import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from .response import CustomResponse
from django.contrib.auth import login, logout


class LoginView(GenericAPIView):
    """Login view for accessing the app"""
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            self.serializer = self.get_serializer(data=request.data)
            self.serializer.is_valid(raise_exception=True)
            self.user = self.serializer.validated_data['user']
            login(request, self.user)
            # generate a token for that user, and login
            refresh = RefreshToken.for_user(self.user)
            user_info = UserSerializer(self.user).data
            return CustomResponse.success(data=user_info, message="Login successful")
        except Exception as e: 
            print(e)
            return CustomResponse.failed(message="Invalid login credentials")


class SignupView(GenericAPIView):
    """Signup View for users"""
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                self.serializer = self.get_serializer(data=request.data)
                self.serializer.is_valid(raise_exception=True)

                first_name = self.serializer.validated_data.get('first_name')
                last_name = self.serializer.validated_data.get('last_name')
                email = self.serializer.validated_data.get('email').lower()
                password = self.serializer.validated_data.get('password')

                # check if a user with the email exists
                if User.objects.filter(email=email).exists():
                    raise Exception("A user with this email address already exists")

                user = User.objects.create_user(email=email,
                    password=password, first_name=first_name,
                    last_name=last_name
                )
                user_info = UserSerializer(user).data

                return CustomResponse.success(
                    data=user_info,
                    message="Registration successful.",
                    status=status.HTTP_201_CREATED
                )
        except Exception as e:
            return CustomResponse.failed(message=str(e))


class TokenRefreshView(GenericAPIView):
    """A view to refresh the access token, by using the refresh token"""
    serializer_class = TokenRefreshSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            self.serializer = self.get_serializer_class()
            self.serializer = self.serializer(data=request.data)
            self.serializer.is_valid(raise_exception=True)
            access_token = self.serializer.save()
            return CustomResponse.success(data=access_token, message="Token refresh successful")
        except Exception as e:
            return CustomResponse.failed(message="Token refresh unsuccessful")


class LogoutView(APIView):
    """View to logout the user"""
    def post(self, request, *args, **kwargs):
        logout(request)
        return CustomResponse.success(message="Logout successful")


class UserViewSet(ModelViewSet):
    """User ViewSet for users"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filterset_class = UserFilter


class BookViewSet(ModelViewSet):
    """Book ViewSet for books"""
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filterset_class = BookFilter


class BorrowedBookViewSet(ModelViewSet):
    """BorrowedBook ViewSet for borrowed books"""
    serializer_class = BorrowedBookSerializer
    queryset = BorrowedBook.objects.all()
    filterset_class = BorrowedBookFilter


class UnavailableBooksView(APIView):
    """List books that are currently borrowed and unavailable for borrowing"""

    def get(self, request):
        unavailable_books = BorrowedBook.objects.filter(returned=False)
        books_data = BorrowedBookSerializer(unavailable_books, many=True).data
        return CustomResponse.success(data=books_data, message="Unavailable books retrieved successfully")
