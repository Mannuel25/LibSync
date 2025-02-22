# LibSync

## Overview
LibSync is a library management system with two APIs:
- **Admin API**: Manages books, users, and borrowing records.
- **Frontend API**: Provides endpoints for users to enroll, browse, and borrow books.

---

## Installation & Setup 🏗️
### 1. Clone the Repository
```sh
git clone https://github.com/Mannuel25/LibSync.git
cd LibSync
```

### 2. Create a `.env` File
Create a `.env` file in the project root and add the required environment variables:
```ini
# General Settings
DEBUG=True
SECRET_KEY=your_secret_key

# Database Settings
NAME=libsync
USER=libsync_user
PASSWORD=libsync_pass
HOST=db
PORT=5432

```

### 3. Build and Start the Containers
```sh
docker-compose up --build -d
```

### 4. Run Migrations
```sh
docker-compose exec frontend_api python manage.py migrate
docker-compose exec admin_api python manage.py migrate
```

---

## Usage 📖
### Access the APIs:
- **Admin API**: `http://localhost:8000/admin_api/`
- **Frontend API**: `http://localhost:8001/frontend_api/`
- **Swagger Docs**:
  - `http://localhost:8000/admin_api/swagger/` for Admin API
  - `http://localhost:8001/frontend_api/swagger/` for Frontend API

### API Endpoints
#### User Enrollment
- **POST** `/frontend_api/register/` → Enroll a new user
- **POST** `/admin_api/login/` → Login a user
- **POST** `/admin_api/logout/` → Logout a user
- **POST** `/admin_api/token/refresh/` → Refresh a user's token

#### Books
- **GET** `/frontend_api/books/` → List available books
- **GET** `/frontend_api/books/{book_id}/` → Get book details
- **PATCH** `/frontend_api/books/{book_id}/` → Update book details
- **DELETE** `/frontend_api/books/{book_id}/` → Delete a book
- **GET** `/frontend_api/books/filter/?category={category}&publisher={publisher}` → Filter books

#### Borrow a Book
- **POST** `/frontend_api/books/borrow/` → Borrow a book
- **GET** `/frontend_api/books/borrowed/` → List borrowed books
- **GET** `/frontend_api/books/borrowed/{borrowed_book_id}/` → Get borrowed book details
- **PATCH** `/frontend_api/books/borrowed/{borrowed_book_id}/` → Update borrowed book details
- **DELETE** `/frontend_api/books/borrowed/{borrowed_book_id}/` → Delete a borrowed book

---

## Running Tests 🧪
To run the test suite, use:
```sh
docker-compose exec admin_api python manage.py test
docker-compose exec frontend_api python manage.py test

```

---

## License 📜
This project is licensed under an [MIT License](LICENSE).

