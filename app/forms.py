from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DecimalField, SelectField, IntegerField, BooleanField, FileField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, NumberRange, Optional, Regexp
import re
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Regexp(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            message='Please enter a valid email address (e.g., user@example.com)'
        )
    ])
    full_name = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=2, max=120)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email address.')
    
    def validate_password(self, password):
        pwd = password.data
        errors = []
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', pwd):
            errors.append('one uppercase letter (A-Z)')
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', pwd):
            errors.append('one lowercase letter (a-z)')
        
        # Check for at least one digit
        if not re.search(r'\d', pwd):
            errors.append('one number (0-9)')
        
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*()_+=\-\[\]{};:\'",.<>?/\\|`~]', pwd):
            errors.append('one special character (!@#$%^&* etc)')
        
        if errors:
            error_msg = 'Password must contain at least: ' + ', '.join(errors)
            raise ValidationError(error_msg)


class LoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')


class BookForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(),
        Length(max=200)
    ])
    author = StringField('Author', validators=[
        DataRequired(),
        Length(max=100)
    ])
    isbn = StringField('ISBN', validators=[
        Optional(),
        Length(min=10, max=13, message='ISBN must be 10-13 characters')
    ])
    cover_image = FileField('Cover Image')
    book_file = FileField('Book File (PDF/ePub)')
    description = TextAreaField('Description', validators=[DataRequired()])
    price = DecimalField('Price ($)', validators=[
        DataRequired(),
        NumberRange(min=0.01, message='Price must be greater than 0')
    ], places=2)
    file_format = SelectField('File Format', choices=[
        ('PDF', 'PDF'),
        ('ePub', 'ePub')
    ], validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    file_path = StringField('File Path', validators=[Optional(), Length(max=255)])


class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[
        ('5', '5 Stars - Excellent'),
        ('4', '4 Stars - Good'),
        ('3', '3 Stars - Average'),
        ('2', '2 Stars - Poor'),
        ('1', '1 Star - Terrible')
    ], validators=[DataRequired()], coerce=int)
    comment = TextAreaField('Review', validators=[
        DataRequired(),
        Length(min=10, max=1000, message='Review must be between 10 and 1000 characters')
    ])


class CheckoutForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[
        DataRequired(),
        Regexp(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            message='Please enter a valid email address'
        )
    ])
    payment_method = SelectField('Payment Method', choices=[
        ('simulated', 'Simulated Payment (Demo)')
    ], validators=[DataRequired()])


class SearchForm(FlaskForm):
    query = StringField('Search Books', validators=[Optional()])
    category = SelectField('Category', coerce=int, validators=[Optional()])
    min_price = DecimalField('Min Price', validators=[Optional(), NumberRange(min=0)], places=2)
    max_price = DecimalField('Max Price', validators=[Optional(), NumberRange(min=0)], places=2)
    sort_by = SelectField('Sort By', choices=[
        ('newest', 'Newest First'),
        ('oldest', 'Oldest First'),
        ('price_low', 'Price: Low to High'),
        ('price_high', 'Price: High to Low'),
        ('rating', 'Highest Rated')
    ], validators=[Optional()])


class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[
        DataRequired(),
        Length(max=50)
    ])
    description = TextAreaField('Description', validators=[Optional()])
