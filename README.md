# Flask Quotes App

A full-stack web application built with **Flask**, **SQLite**, and **SQLAlchemy**, featuring user authentication, dynamic content, and a RESTful API. Users can register, log in, add quotes, and view all submitted quotes in a clean, responsive interface.

---

## 🚀 Features
- **User Authentication**: Account registration, login/logout, and secure session management using Flask-Login.  
- **Database Models**: SQLite + SQLAlchemy ORM with relational tables (`User` ↔ `Quote`).  
- **Template Inheritance**: Jinja2 templates for base layout, forms, and content pages.  
- **Form Handling & Validation**: Input validation, error handling, and flash messaging.  
- **Styling**: Custom CSS for a modern, responsive UI.  
- **API Support**: JSON REST endpoints for accessing quotes (`/api/quotes`).  

---

## 🛠️ Tech Stack
- **Languages**: Python, HTML, CSS  
- **Frameworks/Libraries**: Flask, Flask-SQLAlchemy, Flask-Login, Jinja2, Werkzeug  
- **Database**: SQLite (development)  
- **Tools**: Git, Virtual Environments  

---

## 📂 Project Structure
flask-quotes-app/
│── app.py # main Flask application
│── requirements.txt # dependencies
│── templates/ # Jinja2 HTML templates
│ ├── base.html
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ └── add.html
│── static/ # static assets
│ └── style.css
└── .gitignore

