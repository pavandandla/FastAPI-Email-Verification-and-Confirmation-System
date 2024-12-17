
# **FastAPI Email Verification and Confirmation System**

## **Description**

This project implements a **FastAPI-based Email Verification and Confirmation System** where users must verify their email addresses after registration to access protected features. The system utilizes **JWT tokens** for secure email verification with token expiration mechanisms, ensuring robust security. The solution is designed for scalability, clean organization, and ease of integration with other applications.



## **Features**

- **Robust API Development**  
    Leverages **FastAPI** for building high-performance, asynchronous APIs.
    
- **Secure Authentication**  
    Implements **JWT** for email verification and access control, with token expiration for added security.
    
- **Database Abstraction**  
    Uses **SQLAlchemy** ORM for efficient interaction with **SQLite/MySQL** databases.
    
- **Email Functionality**  
    Sends email verification links using **FastAPI-Mail** with support for **SendGrid** or **SMTP**.
    
- **Password Security**  
    Ensures secure password hashing using **Passlib**.
    
- **Configuration Management**  
    Utilizes **python-dotenv** for environment-based configurations.
    
- **Data Persistence**  
    Stores user data and verification status in a relational database (MySQL/SQLite).
    
## Prerequisites

- Python 3.9+
- pip
- Virtual environment support
## **Libraries Used**

- **FastAPI**
- **SQLAlchemy**
- **JWT**
- **FastAPI-Mail**
- **SendGrid/SMTP**
- **Passlib**
- **python-dotenv**
- **SQLite/MySQL**

## **Installation and Setup**

### **1. Clone the repository**

```bash
git clone https://github.com/pavandandla/FastAPI-Email-Verification-and-Confirmation-System.git
cd FastAPI-Email-Verification-and-Confirmation-System
```

### **2. Create a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate  # For Windows
```

### **3. Install dependencies**

```bash
pip install uv
uv pip install -r src/requirements.txt
```

### **4. Set up the environment variables**

Create a `.env` file in the project root and configure the following:

```plaintext
DATABASE_URL=sqlite:///./test.db  # For SQLite
SMTP_SERVER=smtp.yourprovider.com
SMTP_PORT=587
SMTP_USERNAME=your_email@example.com
SMTP_PASSWORD=your_password
EMAIL_FROM=your_email@example.com
SECRET_KEY=your_secret_key
JWT_EXPIRATION_MINUTES=30
```

### **5. Set up the database**

Run the following command to create the database tables:

```bash
python src/init_db.py
```

### **6. Run the application**

```bash
uvicorn src.app:app --reload
```

The API will be available at: `http://127.0.0.1:8000`
## **Workflow**

1. **User Registration**:
    
    - Users provide an email and password.
    - The system sends a verification email with a **JWT token** in the confirmation link.
2. **Email Verification**:
    
    - The user clicks the email link, and the server verifies the **JWT token**.
    - The user's email is marked as **verified** in the database.
3. **Access Protected Routes**:
    
    - Users with verified emails can access routes protected by authentication.

## **Environment Configuration**

Configure environment variables in the `.env` file for different environments, like

- **SECRET_KEY**: A secure key for JWT encoding/decoding.
## **Contact**

For questions, suggestions, or issues, contact:

- Email: `dandlapavankumar@gmail.com`
- GitHub: [pavandandla](https://github.com/pavandandla)
