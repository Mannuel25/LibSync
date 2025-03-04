from django.urls import re_path as url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

app_name = "admin_mgt"

router.register('users', UserViewSet, basename='users')
router.register('books', BookViewSet, basename='books')
router.register('borrowed_books', BorrowedBookViewSet, basename='borrowed_books')



urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^register/$', RegistrationView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^unavailable_books/$', UnavailableBooksView.as_view(), name='unavailable_books'),
]

