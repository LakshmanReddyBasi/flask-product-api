from flask import Flask, request, jsonify
import flask_mysql_connector
from config import MYSQL_CONFIG

app = Flask(__name__)

#database Conn
app.config['MYSQL_HOST'] = MYSQL_CONFIG['host']
app.config['MYSQL_USER'] = MYSQL_CONFIG['user']
app.config['MYSQL_PASSWORD'] = MYSQL_CONFIG['password']
app.config['MYSQL_DATABASE'] = MYSQL_CONFIG['database']

mysql = flask_mysql_connector.MySQL(app)

# helper function to get a database connection and cursor
def get_db_connection():
    conn = mysql.connection
    cursor = conn.cursor(dictionary=True) #to convert to JSON
    return conn, cursor

#error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error':'Not Found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error':'Bad Request'}), 400

#API Routes

#[GET] /products - for retrieving all the existing products 
@app.route('/products', methods=['GET'])
def get_all_products():
    conn, cursor = get_db_connection()
    try:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        return jsonify(products), 200
    finally:
        cursor.close()
        conn.close()

#[GET] /products/<id> -to get or retrieve a single product by using its ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn, cursor = get_db_connection()
    try:
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product =cursor.fetchone()
        if product is None:
            return jsonify({'message': 'Product not found'}), 404
        return jsonify(product), 200
    finally:
        cursor.close()
        conn.close()

#[POST] /products - for creatinga new product
@app.route('/products',methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or not all(k in data for k in ['name', 'price', 'stock_quantity']):
        return jsonify({'message': 'Missing required fields: name, price, stock_quantity'}), 400

    conn, cursor = get_db_connection()
    try:
        query = """INSERT INTO products (name, description, price, category, stock_quantity, manufacturer, release_date, rating)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        
        cursor.execute(query, (
            data['name'],
            data.get('description'),
            data['price'],
            data.get('category'),
            data['stock_quantity'],
            data.get('manufacturer'),
            data.get('release_date'),
            data.get('rating')
        ))
        conn.commit()
        
        #for getting the new product's ID and return the created product
        new_product_id = cursor.lastrowid
        cursor.execute("SELECT * FROM products WHERE id = %s",(new_product_id,))
        created_product = cursor.fetchone()

        return jsonify({'message': 'Product added successfully', 'product': created_product}),201
    finally:
        cursor.close()
        conn.close()

#[PUT] /products/<id> - for updating an existing product
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}),400

    conn, cursor = get_db_connection()
    try:
        #Check if product exists already in the db
        cursor.execute("SELECT * FROM products WHERE id = %s",(product_id,))
        if cursor.fetchone() is None:
            return jsonify({'message': 'Product not found'}),404
        
        # Construct the SET part of the SQL query dynamically
        update_fields = ', '.join([f"{key} = %s" for key in data.keys()])
        update_values = list(data.values())
        update_values.append(product_id) 
        
        query = f"UPDATE products SET {update_fields} WHERE id = %s"
        
        cursor.execute(query, tuple(update_values))
        conn.commit()

        # Fetch and return the updated product
        cursor.execute("SELECT * FROM products WHERE id = %s",(product_id,))
        updated_product = cursor.fetchone()
        
        return jsonify({'message':'Product updated successfully','product':updated_product}),200
    finally:
        cursor.close()
        conn.close()

#[DELETE] /products/<id> - Delete a product
@app.route('/products/<int:product_id>',methods=['DELETE'])
def delete_product(product_id):
    conn, cursor = get_db_connection()
    try:
        # Check if product exists before deleting
        cursor.execute("SELECT * FROM products WHERE id = %s",(product_id,))
        if cursor.fetchone() is None:
            return jsonify({'message':'Product not found'}), 404

        cursor.execute("DELETE FROM products WHERE id = %s",(product_id,))
        conn.commit()
        return jsonify({'message':'Product deleted successfully'}),200
    finally:
        cursor.close()
        conn.close()

if __name__=='__main__':
    app.run(debug=True) 