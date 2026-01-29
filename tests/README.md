# CyberBooks Unit Tests

This directory contains unit tests for the CyberBooks application using pytest.

## Test Coverage

The test suite covers the following main functionalities:

### 1. User Registration
- Registration page loads
- Successful user registration
- Duplicate username prevention
- Duplicate email prevention
- Password mismatch validation

### 2. User Login
- Login page loads
- Successful login
- Wrong password rejection
- Non-existent user rejection
- User logout
- Protected page access control

### 3. Add to Cart
- Login requirement for cart
- Successfully adding book to cart
- Preventing duplicate books in cart
- Viewing cart
- Removing items from cart

### 4. Write Review
- Login requirement for reviews
- Purchase requirement for reviews
- Successful review submission
- Duplicate review prevention

### 5. Error Pages
- 404 page
- 403 forbidden page

### 6. Book Listing
- Shop page loads
- Books appear in shop
- Book detail page loads
- Home page loads

## Running Tests

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Run all tests:
```bash
pytest tests/test_app.py -v
```

### Run specific test:
```bash
pytest tests/test_app.py::test_successful_registration -v
```

### Run tests with coverage:
```bash
pytest tests/test_app.py --cov=app -v
```

## Test Database

Tests use an in-memory SQLite database configured in `config.py` under `TestingConfig`:
- Database: `sqlite:///:memory:`
- CSRF protection disabled for easier testing
- No persistent data

## Requirements

- pytest
- pytest-flask

All required packages are in `requirements.txt`.
