from flask import Flask, request, jsonify
import os
import pymysql

app = Flask(__name__)

# Azure SQL Server Configuration
# Use environment variables for security
username = os.environ.get("DB_USERNAME", "rootadmin")
password = os.environ.get("DB_PASSWORD", "P@#sword01")
server = os.environ.get("DB_SERVER", "mysqlserver0001.database.windows.net")
database = os.environ.get("DB_NAME", "testpoc0001")

def get_conn():
    return pymysql.connect(
        host=os.environ.get("DB_SERVER"),
        user=os.environ.get("DB_USERNAME"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        port=3306
    )

@app.route('/')
def index():
    return "Flask API Running on Azure!"

@app.route("/category/post", methods=["POST"])
def category_post():
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        c_name = request.json["c_name"]
        cur.execute("INSERT INTO category (c_name) OUTPUT INSERTED.c_id VALUES (%s)", (c_name,))
        last_inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Data added successfully", "c_id": last_inserted_id}), 201
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/category/get/<cat_id>", methods=["GET"])
def category_get(cat_id):
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM category WHERE c_id=%s", (cat_id,))
        data = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()
        
        if not data:
            return jsonify({"message": "Data not found due to invalid category id"}), 404
        
        result = [dict(zip(column_names, row)) for row in data]
        return jsonify(result[0])
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/category/put/<user_id>", methods=["PUT"])
def category_put(user_id):
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        c_name = request.json["c_name"]
        cur.execute("UPDATE category SET c_name=%s WHERE c_id=%s", (c_name, user_id))
        conn.commit()
        updated = cur.rowcount
        cur.close()
        conn.close()
        
        if updated == 0:
            return jsonify({"message": "Data not updated"}), 404
        return jsonify({"message": "Data updated successfully"})
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/category/delete/<user_id>", methods=["DELETE"])
def category_delete(user_id):
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT c_id FROM subcategory WHERE c_id=%s", (user_id,))
        subcategory_id = cur.fetchone()
        if subcategory_id:
            cur.close()
            conn.close()
            return jsonify({"message": "Category id is used in subcategory table so can't delete it"}), 400
        
        cur.execute("DELETE FROM category WHERE c_id=%s", (user_id,))
        conn.commit()
        deleted = cur.rowcount
        cur.close()
        conn.close()
        
        if deleted == 0:
            return jsonify({"message": "Data not deleted"}), 404
        return jsonify({"message": "Data deleted successfully"})
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/subcategory/post", methods=["POST"])
def subcategory_post():
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        s_name = request.json["s_name"]
        c_id = request.json["c_id"]
        cur.execute("INSERT INTO subcategory (s_name, c_id) VALUES (%s, %s)", (s_name, c_id))
        cur.execute("SELECT @@IDENTITY")
        last_inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Data added successfully", "s_id": last_inserted_id}), 201
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/subcategory/get/<user_id>", methods=["GET"])
def subcategory_get(user_id):
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM subcategory WHERE s_id=%s", (user_id,))
        data = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()
        
        if not data:
            return jsonify({"message": "Data not found due to invalid id"}), 404
        
        result = [dict(zip(column_names, row)) for row in data]
        return jsonify(result[0])
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/subcategory/put/<user_id>", methods=["PUT"])
def subcategory_put(user_id):
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        s_name = request.json["s_name"]
        cur.execute("UPDATE subcategory SET s_name=%s WHERE s_id=%s", (s_name, user_id))
        conn.commit()
        updated = cur.rowcount
        cur.close()
        conn.close()
        
        if updated == 0:
            return jsonify({"message": "Data not updated"}), 404
        return jsonify({"message": "Data updated successfully"})
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/subcategory/delete/<user_id>", methods=["DELETE"])
def subcategory_delete(user_id):
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT s_id FROM product WHERE s_id=%s", (user_id,))
        product_id = cur.fetchone()
        if product_id:
            cur.close()
            conn.close()
            return jsonify({"message": "s_id is used in product table so can't delete it"}), 400
        
        cur.execute("DELETE FROM subcategory WHERE s_id=%s", (user_id,))
        conn.commit()
        deleted = cur.rowcount
        cur.close()
        conn.close()
        
        if deleted == 0:
            return jsonify({"message": "Enter valid id"}), 404
        return jsonify({"message": "Data deleted successfully"})
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/product/post", methods=["POST"])
def product_post():
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        p_name = request.json["p_name"]
        p_description = request.json["p_description"]
        s_id = request.json["s_id"]
        making_date = request.json["making_date"]
        batch_no = request.json["batch_no"]
        cur.execute("INSERT INTO product (p_name, p_description, s_id, making_date, batch_no) VALUES (%s, %s, %s, %s, %s)", (p_name, p_description, s_id, making_date, batch_no))
        cur.execute("SELECT @@IDENTITY")
        last_inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Data added successfully", "p_id": last_inserted_id}), 201
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/product/get/<user_id>", methods=["GET"])
def product_get(user_id):
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM product WHERE p_id=%s", (user_id,))
        data = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()
        
        if not data:
            return jsonify({"message": "Data not found. Enter valid id"}), 404
        
        result = [dict(zip(column_names, row)) for row in data]
        return jsonify(result[0])
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/product/put/<user_id>", methods=["PUT"])
def product_put(user_id):
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        p_name = request.json["p_name"]
        cur.execute("UPDATE product SET p_name=%s WHERE p_id=%s", (p_name, user_id))
        conn.commit()
        updated = cur.rowcount
        cur.close()
        conn.close()
        
        if updated == 0:
            return jsonify({"message": "Data not updated"}), 404
        return jsonify({"message": "Data updated successfully"})
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/product/delete/<user_id>", methods=["DELETE"])
def product_delete(user_id):
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT p_id FROM inventory WHERE p_id=%s", (user_id,))
        inventory_id = cur.fetchone()
        if inventory_id:
            cur.close()
            conn.close()
            return jsonify({"message": "p_id is used in inventory table so can't delete it"}), 400
        
        cur.execute("DELETE FROM product WHERE p_id=%s", (user_id,))
        conn.commit()
        deleted = cur.rowcount
        cur.close()
        conn.close()
        
        if deleted == 0:
            return jsonify({"message": "Data not deleted. Enter valid id"}), 404
        return jsonify({"message": "Data deleted successfully"})
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/inventory/post", methods=["POST"])
def inventory_post():
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        p_id = request.json["p_id"]
        p_name = request.json["p_name"]
        quantity = request.json["quantity"]
        price = request.json["price"]
        cur.execute("INSERT INTO inventory (p_id, p_name, quantity, price) VALUES (%s, %s, %s, %s)", (p_id, p_name, quantity, price))
        cur.execute("SELECT @@IDENTITY")
        last_inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Data added successfully", "i_id": last_inserted_id}), 201
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/inventory/get/<user_id>", methods=["GET"])
def inventory_get(user_id):
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory WHERE p_id=%s", (user_id,))
        data = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()
        
        if not data:
            return jsonify({"message": "Data not found. Enter correct id"}), 404
        
        result = [dict(zip(column_names, row)) for row in data]
        return jsonify(result[0])
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/inventory/put/<user_id>", methods=["PUT"])
def inventory_put(user_id):
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        p_name = request.json["p_name"]
        quantity = request.json["quantity"]
        cur.execute("UPDATE inventory SET p_name=%s, quantity=%s WHERE p_id=%s", (p_name, quantity, user_id))
        conn.commit()
        updated = cur.rowcount
        cur.close()
        conn.close()
        
        if updated == 0:
            return jsonify({"message": "Data not updated"}), 404
        return jsonify({"message": "Data updated successfully"})
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/inventory/delete/<user_id>", methods=["DELETE"])
def inventory_delete(user_id):
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT p_id FROM sales WHERE p_id=%s", (user_id,))
        sales_p_id = cur.fetchone()
        if sales_p_id:
            cur.close()
            conn.close()
            return jsonify({"message": "p_id is used in sales table so can't delete p_id"}), 400
        
        cur.execute("DELETE FROM inventory WHERE p_id=%s", (user_id,))
        conn.commit()
        deleted = cur.rowcount
        cur.close()
        conn.close()
        
        if deleted == 0:
            return jsonify({"message": "Data not deleted. Enter correct id"}), 404
        return jsonify({"message": "Data deleted successfully"})
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/customer/post", methods=["POST"])
def customer_post():
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        customer_name = request.json["customer_name"]
        customer_pn = request.json["customer_pn"]
        cur.execute("INSERT INTO customer (customer_name, customer_pn) VALUES (%s, %s)", (customer_name, customer_pn))
        cur.execute("SELECT @@IDENTITY")
        last_inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Data added successfully", "customer_id": last_inserted_id}), 201
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/customer/get/<user_id>", methods=["GET"])
def customer_get(user_id):
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM customer WHERE customer_id=%s", (user_id,))
        data = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()
        
        if not data:
            return jsonify({"message": "Data not found. Enter valid id"}), 404
        
        result = [dict(zip(column_names, row)) for row in data]
        return jsonify(result[0])
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/customer/put/<user_id>", methods=["PUT"])
def customer_put(user_id):
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        customer_name = request.json["customer_name"]
        customer_pn = request.json["customer_pn"]
        cur.execute("UPDATE customer SET customer_name=%s, customer_pn=%s WHERE customer_id=%s", (customer_name, customer_pn, user_id))
        conn.commit()
        updated = cur.rowcount
        cur.close()
        conn.close()
        
        if updated == 0:
            return jsonify({"message": "Data not updated. Enter valid id"}), 404
        return jsonify({"message": "Data updated successfully"})
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/customer/delete/<user_id>", methods=["DELETE"])
def customer_delete(user_id):
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT customer_id FROM sales WHERE customer_id=%s", (user_id,))
        customer_id = cur.fetchone()
        if customer_id:
            cur.close()
            conn.close()
            return jsonify({"message": "Customer id is used in sales table so can't delete customer id"}), 400
        
        cur.execute("DELETE FROM customer WHERE customer_id=%s", (user_id,))
        conn.commit()
        deleted = cur.rowcount
        cur.close()
        conn.close()
        
        if deleted == 0:
            return jsonify({"message": "Data not deleted. Enter valid id"}), 404
        return jsonify({"message": "Data deleted successfully"})
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/sales/post", methods=["POST"])
def sales_post():
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        p_id = request.json["p_id"]
        customer_id = request.json["customer_id"]
        units_purchased = request.json["units_purchased"]
        
        cur.execute("SELECT quantity FROM inventory WHERE p_id = %s", (p_id,))
        result = cur.fetchone()
        if not result:
            cur.close()
            conn.close()
            return jsonify({"message": "Product not found"}), 404
        
        current_stock = result[0]
        if units_purchased > current_stock:
            cur.close()
            conn.close()
            return jsonify({"message": "Insufficient stock"}), 400
        
        new_stock = current_stock - units_purchased
        cur.execute("INSERT INTO sales (p_id, customer_id, units_purchased, stock_after_purchase) VALUES (%s, %s, %s, %s)", (p_id, customer_id, units_purchased, new_stock))
        cur.execute("UPDATE inventory SET quantity = %s WHERE p_id = %s", (new_stock, p_id))
        cur.execute("SELECT @@IDENTITY")
        last_inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Data added successfully", "sales_id": last_inserted_id}), 201
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/sales/get/<user_id>", methods=["GET"])
def sales_get(user_id):
    conn = get_conn()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM sales WHERE sales_id = %s", (user_id,))
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()
        
        if not rows:
            return jsonify({"message": "Data not found. Enter a valid ID"}), 404
        
        data = [dict(zip(column_names, row)) for row in rows]
        return jsonify(data[0])
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Use Azure's PORT environment variable or default to 8000
    port = int(os.environ.get("PORT", 8000))
    print(f"Inventory Management System is running on port {port}")
    app.run(host="0.0.0.0", port=port) 