# E-miti Inventory System

E-miti Inventory System is a command-line based pharmacy inventory management system built using Python and Urwid. It allows users to manage inventory items, user registrations, and authentication. The inventory data is stored in a MySQL database.

## Features

- User Registration and Authentication
- Add, Update, Delete, Search, and Flag Inventory Items
- User Role Management (Admin, Pharmacist, Inventory Manager, Hospital)
- Inventory Item Expiry Date Management
- Inventory Item Flagging for Special Attention
- Top Users for Specific Inventory Item

## Installation

### Prerequisites

- Python 3.x
- MySQL server
- pip (Python package installer)

### Steps

1. Clone the repository:
    sh
    git clone <repository-url>
    cd e-miti
    

2. Create and activate a virtual environment:
    sh
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    

3. Install the required dependencies:
    sh
    pip install -r requirements.txt
    

4. Set up the MySQL database:
    - Create a MySQL database and user.
    - Run the following SQL commands to set up the tables:
      sql
      CREATE DATABASE e_miti_db;
      USE e_miti_db;

      CREATE TABLE users (
          id INT AUTO_INCREMENT PRIMARY KEY,
          username VARCHAR(255) UNIQUE NOT NULL,
          password VARCHAR(255) NOT NULL,
          role VARCHAR(50) NOT NULL
      );

      CREATE TABLE inventory (
          id INT AUTO_INCREMENT PRIMARY KEY,
          user_id INT NOT NULL,
          name VARCHAR(255) NOT NULL,
          quantity INT NOT NULL,
          price DECIMAL(10, 2) NOT NULL,
          code VARCHAR(50) NOT NULL,
          expiry_date DATETIME NOT NULL,
          created_at DATETIME NOT NULL,
          flag BOOLEAN DEFAULT FALSE,
          FOREIGN KEY (user_id) REFERENCES users(id)
      );
      

5. Set up environment variables:
    - Create a .env file in the project root and add your database configuration:
      env
      DB_HOST=your_db_host
      DB_USER=your_db_user
      DB_PASSWORD=your_db_password
      DB_NAME=e_miti_db
      

## Running the Application

To run the application, execute the following command:
```sh
python main.py
Project Structure
plaintext
Copy code
e-miti/
│
├── main.py                # Main entry point of the application
├── user_management.py     # User management logic
├── user_database.py       # User database interaction logic
├── inventory_management.py# Inventory management logic
├── inventory_database.py  # Inventory database interaction logic
├── requirements.txt       # Python package dependencies
├── .env                   # Environment variables (ignored in version control)
└── README.md              # This README file
Usage
Main Menu:

Register
Login
Exit
Inventory Menu (after login):

Add Item
Update Item
Delete Item
Search Item
Flag Item
Logout
Adding an Item:

Enter the name, quantity, price, code, expiry date, and flag status of the item.
Updating an Item:

Enter the item ID, and new values for name, quantity, price, code, and expiry date.
Deleting an Item:

Enter the item ID to delete it from the inventory.
Searching for an Item:

Enter the item name to search for top users who have that item in inventory.
Flagging an Item:

Enter the item ID to flag it for special attention.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Urwid: A library for creating terminal-based user interfaces in Python.
MySQL: An open-source relational database management system.
Python: A high-level programming language for general-purpose programming.