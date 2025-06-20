# 🗃️ Inventory Management System

This is a full-stack Inventory Management System built using **Flask** (Python) and **MySQL**, with an interactive **HTML + Bootstrap** frontend. It allows CRUD operations on categories, subcategories, products, inventory, customers, and sales.

---

## 🚀 Features

- 🔐 JWT Authentication for secure API access
- 🔄 CRUD operations on:
  - Category
  - Subcategory
  - Product
  - Inventory
  - Customer
  - Sales
- 📦 Real-time stock management
- 📊 Simple Bootstrap interface for easy navigation
- 🔌 RESTful API structure
- 📁 Clean and modular code structure

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** MySQL
- **Frontend:** HTML, Bootstrap, JavaScript
- **Authentication:** JWT (JSON Web Tokens)

---

## 🗂️ Project Structure

inventory-system/
│
├── app.py # Main Flask app
├── config.py # Configuration for DB and JWT
├── models/ # DB models and queries
├── routes/ # All CRUD API routes
├── templates/ # HTML frontend files
├── static/ # Bootstrap and custom CSS/JS
└── README.md # Project documentation

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/inventory-management-system.git
cd inventory-management-system
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Configure MySQL Database
Update the config.py file with your MySQL credentials:

python
Copy
Edit
MYSQL_HOST = 'localhost'
MYSQL_USER = 'your_username'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'product'
SECRET_KEY = 'your_jwt_secret_key'
4. Run the Application
bash
Copy
Edit
python app.py
📬 API Endpoints
Resource	Endpoint	Method
Category	/api/categories	GET, POST
/api/categories/<id>	PUT, DELETE
Subcategory	/api/subcategories	GET, POST
Product	/api/products	GET, POST
Inventory	/api/inventory	GET, POST
Customer	/api/customers	GET, POST
Sales	/api/sales	GET, POST
Auth	/login	POST

🔐 Authentication
JWT token is required for all API endpoints.

Token is returned on successful login and should be passed in the Authorization header:

makefile
Copy
Edit
Authorization: Bearer <your_token>
📷 Screenshots
You can insert UI screenshots here if needed.

✍️ Author
Sarvagya Jain