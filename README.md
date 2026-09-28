# Python Quiz Hub

Python Quiz Hub is a web-based quiz application developed as a student project using Python and FastAPI.

The application allows users to register and log in, access a dashboard, attempt Python quizzes on different topics and difficulty levels, and view their quiz results.

## Features

- User Registration
- User Login and Logout
- PostgreSQL database for user information
- SQLAlchemy for database interaction
- Session-based authentication
- User Dashboard
- User Profile
- Multiple Python Quiz Topics
- Quiz Timer
- Quiz Submission Confirmation
- Automatic quiz submission when time ends
- Quiz Score Calculation
- Quiz Result Page
- User-specific score viewing
- Responsive and clean user interface

## Quiz Topics

The project currently includes quizzes covering:

- Python Basics
- Variables and Data Types
- Functions
- Exception Handling
- File Handling
- Advanced Python

## Technologies Used

### Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL

### Frontend

- HTML
- CSS
- JavaScript
- Jinja2 Templates

### Database

- PostgreSQL
- SQLAlchemy ORM

## Project Structure

```text
python_quiz_hub/
│
├── main.py
├── README.md
├── requirements.txt
│
├── static/
│   ├── style.css
│   └── jsfiles/
│       ├── quiz.js
│       ├── login.js
│       ├── profile.js
│       └── dashboard.js
│
└── templates/
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── profile.html
    ├── basic.html
    ├── variable.html
    ├── function.html
    ├── exception.html
    ├── file.html
    ├── advance.html
    └── result.html
