# Product Management API - Flask Assignment

This project is a REST API for managing a product inventory, built with Python and Flask.

## Setup and Installation

### Prerequisites
- Python 3.x
- MySQL Server
- Postman (for testing)

### 1.Clone the Repository & Setup Virtual Environment
```bash
# It's recommended to use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 2. Install Dependencies
Install all the required Python packages using the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### 3. Database Setup
1.  Connect to your MySQL server.
2.  Create a database for the project (e.g., `product_db`).
3.  **Important**: Select your newly created database (`USE product_db;`).
4.  Run the entire `database.sql` script to create the `products` table and insert sample data.

### 4. Configure Database Connection
Open the `config.py` file and update the `MYSQL_CONFIG` dictionary with your MySQL username, password, and the database name you created.

## How to Run the Application
Once the setup is complete, run the Flask application with the following command:
```bash
python app.py
```
The server will start on `http://127.0.0.1:5000`.
then go to the products route-- `http://127.0.0.1:5000/products`
there , you can see the data present in our database

## Testing the API
The `Product_API.postman_collection.json` file can be imported into Postman to test all the available API endpoints.