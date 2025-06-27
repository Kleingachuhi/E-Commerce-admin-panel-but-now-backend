# E-Commerce-Admin-Panel-Backend

A complete RESTful API for an e-commerce platform with user authentication, product management, and admin functionality.

## Features

- 🔐 JWT Authentication
- 👥 User roles (admin/user)
- 🛍️ Product catalog management
- 📦 Product variants (items)
- 📊 Audit logging
- 🔄 Database migrations
- ✅ Input validation
- 📝 Comprehensive documentation

## Tech Stack

- **Framework**: Flask
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **Authentication**: JWT
- **Password Hashing**: Bcrypt
- **API Documentation**: Postman collection

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone "git@github.com:Kleingachuhi/E-Commerce-admin-panel-but-now-backend.git"
   cd "E-Commerce-admin-panel-but-now-backend"

2. Create and activate virtual environment:
    pipenv install flask flask_sqlalchemy flask_migrate flask-jwt-extended psycopg2-binary 
    pipenv shell

3. Install dependencies:
    pip install -r requirements.txt

4. Set up environment variables:
   cp .env.example .env
   Edit .env with your configuration.

5. Initialize database:
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade

6. Seed initial data:
   python seed.py

7. Running the API:
   python run.py

## API Endpoints
Authentication
Method	Endpoint	Description
POST	/api/auth/register	Register new user
POST	/api/auth/login	Login user

Products
Method	Endpoint	Description
GET	/api/products	Get paginated products
POST	/api/products	Create new product

Categories
Method	Endpoint	Description
GET	/api/categories	Get all categories
POST	/api/categories	Create new category

Admin
Method	Endpoint	Description
GET	/api/admin/users	List all users (admin)
GET	/api/admin/audit-logs	View audit logs (admin)

# Sample testing in Postman
Import the Postman collection (link to your exported collection) with these sample requests:

Successful Flows

Register User
POST /api/auth/register
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!"
}

Login User
POST /api/auth/login
Content-Type: application/json

{
    "username": "testuser",
    "password": "SecurePass123!"
}

Access Protected Route
GET /api/protected
Authorization: Bearer <access_token>

# Technologies used
1. Python 3.8+
2. Flask
3. Flask-SQLAlchemy
4. Flask-JWT-Extended
5. Flask-Cors
6. Flask-Bcrypt

# Deployment
-Deploy the backend on Render and connect the backend to the frontend.The frontend should be able to fetch data not from the frontend Json but from the backend.

## License
Copyright <2025> <Kelly>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


