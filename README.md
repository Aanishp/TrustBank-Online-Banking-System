# 💵 TrustBank Online Banking System
TrustBank: Online Banking System
This project is a fully functional web-based online banking application developed by a team of four as a DBMS mini-project. It simulates a real-world banking environment where users can manage their accounts, perform transactions, and view their financial history in a secure and user-friendly interface.

The application is built with a Python Flask backend, uses SQLAlchemy for object-relational mapping, and connects to a MySQL database. The frontend is designed with HTML, CSS, and Bootstrap 5 for a responsive user experience.

---

## ✨ **Features**
- Secure User Authentication: Users can sign up for a new account and log in securely. Passwords are fully hashed for protection.
- Account Management: Users can create multiple types of bank accounts (e.g., Savings, Current) linked to their profile.
- Core Banking Operations:
   - Deposit: Add funds to any of their accounts.
   - Withdraw: Withdraw money, with checks to prevent overdrawing.
- Transfer: Securely transfer funds between any two accounts in the system.
- Transaction History: A detailed and chronological view of all past transactions, including payments sent and received.
- Profile Management: Users can view their personal details and a list of all their associated bank accounts.

---

## 💻 **Tech Stack**
- **Backend:** Python, Flask
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Authentication:** Flask-Login, Werkzeug (for password hashing)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5

---

## 🚀 **Getting Started**
Follow these instructions to set up and run the project locally.
### **Prerequisites**
- Python 3.7+
- A MySQL server (e.g., from XAMPP or a standalone installation)

### 🔹 1️⃣ Clone the Repository  
```bash
git clone https://github.com/Aanishp/TrustBank-Online-Banking-System.git
cd TrustBank-Online-Banking-System
```

### 🔹 2️⃣ Create the MySQL Database Connect to your MySQL server and run the following command to create the database:
```sql
CREATE DATABASE bank_database;
```

### 🔹 3️⃣ Set Up a Virtual Environment It's highly recommended to use a virtual environment.
```bash
# For venv
python -m venv env
env\Scripts\activate

# Or for Conda
conda create -n bankenv python=3.9
conda activate bankenv
```

### 🔹 4️⃣ Install Dependencies Install all the required packages from the requirements.txt file.
```bash
pip install -r requirements.txt
```

### 🔹 5️⃣ Run the Application Execute the main Python script to start the Flask server. The tables will be created automatically on the first run.
```bash
python main.py
```

### 🔹 6️⃣ Access the Application Open your web browser and navigate to:
```bash
http://127.0.0.1:5000
```

---

## 👥 Team Members  
🚀 [Aanish P](https://github.com/Aanishp)  
🚀 [](https://github.com/prajwal50)  
🚀 [](https://github.com/Harshith1320)  
🚀 [](https://github.com/vijayvarmastr-11)  

---

📍 **Department of Artificial Intelligence & Machine Learning**  
📍 **BMS Institute of Technology & Management, Bengaluru** 

---
