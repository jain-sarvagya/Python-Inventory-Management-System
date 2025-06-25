# from flask import Flask, request, jsonify
# import pyodbc
# import os
# from azure import identity

# #P@#sword01

# app = Flask(__name__)
# # mysql=app(MySQL)

# username = "rootadmin"
# password = "P@#sword01"
# server = "mysqlserver0001.database.windows.net" 
# database = "testpoc0001"

# # connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]
# connection_string="Driver={SQL Server};Server=tcp:mysqlserver0001.database.windows.net,1433;Database=testpoc0001;Uid=rootadmin;Pwd=P@#sword01;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

# def get_conn():
#     # credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
#     # token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
#     # token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
#     SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
#     conn = pyodbc.connect(connection_string)
#     return conn
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# conn = get_conn()

# @app.route('/')
# def index():
#     return "Flask Api Running!"



# @app.route("/category/post", methods=["POST"])
# def category_post():
    
#         cur = conn.cursor()
#         c_name = request.json["c_name"]

#         cur.execute("INSERT INTO category (c_name) OUTPUT INSERTED.c_id VALUES (?)", (c_name,))

#         # Get the last inserted ID (optional, but useful for knowing which ID was assigned)
#         cur.execute("SELECT @@IDENTITY")
#         last_inserted_id = cur.fetchone()[0]
#         conn.commit()
#         cur.close()
#         return jsonify({"message": "Data added successfully", "c_id": last_inserted_id}), 201



# #get method of category

# @app.route("/category/get/<cat_id>",methods=["get"])
# def category_get(cat_id):
#     cur=conn.cursor()
#     result=cur.execute("select * from category where c_id=?",(cat_id,))
#     data=cur.fetchall()
#     column_name=[disc[0] for disc in cur.description]
#     cur.close()
#     for row in data:
#         data=dict(zip(column_name,row))
#     if result==0:
#         return jsonify({"message":"data not found due to invalid category id"})
#     return jsonify(data)

# #put method of category

# @app.route("/category/put/<user_id>",methods=["put"])
# def category_put(user_id):
#     cur=conn.cursor()
#     c_name=request.json["c_name"]
#     result=cur.execute("update category set c_name=? where c_id=? ",(c_name,user_id))
#     print(result)
#     conn.commit()
#     if result==0:
#         return jsonify ({"message":"data not updated"})
#     cur.close()
#     return jsonify({"message":"data update successfully"})

# #delete method of category

# @app.route("/category/delete/<user_id>",methods=["delete"])
# def category_delete(user_id):
#     cur=conn.cursor()
#     cur.execute("select c_id from Subcategory where c_id=?",(user_id))
#     Subcategory_id=cur.fetchone()
#     if Subcategory_id:
#         cur.close()
#         return jsonify({"message":"category id uses in Subcategory table so can't delete it"})
#     cur.execute("delete from category where c_id=?",(user_id))
#     conn.commit()
#     if cur.rowcount==0:
#         cur.close()
#         return jsonify({"message":"data not delete"})
#     cur.close()
#     return jsonify ({"message":"data delete successfully"})

# #post method of Subcategory

# @app.route("/subcategory/post",methods=["post"])
# def subcategory_post():
#     cur=conn.cursor()
#     S_name=request.json["S_name"]
#     c_id=request.json["c_id"]
#     cur.execute("insert into Subcategory (S_name,c_id) values (?,?)",(S_name,c_id))
#     # Get the last inserted ID (optional, but useful for knowing which ID was assigned)
#     cur.execute("SELECT @@IDENTITY")
#     last_inserted_id = cur.fetchone()[0]
#     conn.commit()
#     cur.close()
#     return jsonify({"message": "Data added successfully", "s_id": last_inserted_id}), 201

# #get method of Subcategory

# @app.route("/subcategory/get/<user_id>",methods=["get"])
# def subcategory_get(user_id):
#     cur=conn.cursor()
#     result=cur.execute("select * from Subcategory where s_id=?",(user_id))
#     data=cur.fetchall()
#     column_name=[disc[0] for disc in cur.description]
#     cur.close()
#     for row in data:
#         data=dict(zip(column_name,row))
#     if result==0:
#         return jsonify({"message":"data not found due to invalid id"})
#     return jsonify(data)

# #put method of Subcategory

# @app.route("/subcategory/put/<user_id>",methods=["put"])
# def subcategory_put(user_id):
#     cur=conn.cursor()
#     s_name=request.json["s_name"]
#     result=cur.execute("update Subcategory set s_name=%s where s_id=%s",(s_name,user_id))
#     conn.commit()
#     cur.close()
#     if result==0:
#         return jsonify({"message":"data not updated"})
#     return jsonify({"message":"data update successfully"})

# #delete method of Subcategory

# @app.route("/subcategory/delete/<user_id>",methods=["delete"])
# def subcategory_delete(user_id):
#     cur=conn.cursor()
#     cur.execute("select s_id from product where s_id=?",(user_id))
#     product_id=cur.fetchone()
#     if product_id:
#         return jsonify ({"message":"s_id is using in product table so can't delete it"})
#     result=cur.execute("delete from Subcategory where s_id=?",(user_id))
#     conn.commit()
#     cur.close()
#     if result==0:
#         return jsonify({"message":"enter valid id"})
#     return jsonify ({"message":"data delete successfully"})

# #post method of product

# @app.route("/product/post",methods=["post"])
# def product_post():
#     cur=conn.cursor()
#     p_name=request.json["p_name"]
#     p_description=request.json["p_description"]
#     s_id=request.json["s_id"]
#     making_date=request.json["making_date"]
#     batch_no=request.json["batch_no"]
#     cur.execute("insert into product (p_name,p_description,s_id,making_date,batch_no) values (?,?,?,?,?)",(p_name,p_description,s_id,making_date,batch_no))
#     # Get the last inserted ID (optional, but useful for knowing which ID was assigned)
#     cur.execute("SELECT @@IDENTITY")
#     last_inserted_id = cur.fetchone()[0]
#     conn.commit()
#     cur.close()
#     return jsonify({"message": "Data added successfully", "p_id": last_inserted_id}), 201

# #get method of product

# @app.route("/product/get/<user_id>",methods=["get"])
# def product_get(user_id):
#     cur=conn.cursor()
#     result=cur.execute("select * from product where p_id=?",(user_id))
#     data=cur.fetchall()
#     column_name=[disc[0] for disc in cur.description]
#     cur.close()
#     for row in data:
#         data=dict(zip(column_name,row))
#     if result==0:
#         return jsonify({"message":"data not found enter valid id"})
#     return jsonify(data)

# #put method of product

# @app.route("/product/put/<user_id>",methods=["put"])
# def product_put(user_id):
#     cur=conn.cursor()
#     p_name=request.json["p_name"]
#     result=cur.execute("update product set p_name=? where p_id=?",(p_name,user_id))
#     conn.commit()
#     cur.close()
#     if result==0:
#         return jsonify({"message":"data not updated"})
#     return jsonify({"message":"data update successfully"})

# #delete method of product

# @app.route("/product/delete/<user_id>",methods=["delete"])
# def product_delete(user_id):
#     cur=conn.cursor()
#     cur.execute("select p_id from inventory where p_id=?",(user_id))
#     invenory_id=cur.fetchone()
#     if invenory_id:
#         return jsonify({"message":"p_id is using in inventory table so can't delete it"})
#     result=cur.execute("delete from product where p_id=?",(user_id))
#     conn.commit()
#     cur.close()
#     if result==0:
#         return jsonify({"message":"data not deleted enter valid id"})
#     return jsonify ({"message":"data delete s+uccessfully"})

# #post method for inventory

# @app.route("/inventory/post",methods=["post"])
# def inventory_post():
#     cur=conn.cursor()
#     p_id=request.json["p_id"]
#     p_name=request.json["p_name"]
#     quantity=request.json["quantity"]
#     price=request.json["price"]
#     cur.execute("insert into inventory (p_id,p_name,quantity,price) values (?,?,?,?)",(p_id,p_name,quantity,price))
#     # Get the last inserted ID (optional, but useful for knowing which ID was assigned)
#     cur.execute("SELECT @@IDENTITY")
#     last_inserted_id = cur.fetchone()[0]
#     conn.commit()
#     cur.close()
#     return jsonify({"message": "Data added successfully", "i_id": last_inserted_id}), 201
# #get method of inventory

# @app.route("/inventory/get/<user_id>",methods=["get"])
# def inventory_get(user_id):
#     cur=conn.cursor()
#     result=cur.execute("select * from inventory where p_id=?",(user_id))
#     data=cur.fetchall()
#     column_name=[disc[0] for disc in cur.description]
#     cur.close()
#     for row in data:
#         data=dict(zip(column_name,row))
#     if result==0:
#         return jsonify({"messsage":"data not found enter correct id"})
#     return jsonify(data)

# #put method of inventory

# @app.route("/inventory/put/<user_id>",methods=["put"])
# def inventory_put(user_id):
#     cur=conn.cursor()
#     p_name=request.json["p_name"]
#     quantity=request.json["quantity"]
#     result=cur.execute("update inventory set p_name=?,quantity=? where p_id=?",(p_name,quantity,user_id))
#     conn.commit()
#     cur.close()
#     if result==0:
#         return jsonify({"message":"data not updated"})
#     return jsonify({"message":"data update successfully"})

# #delete method of inventory

# @app.route("/inventory/delete/<user_id>",methods=["delete"])
# def inventory_delete(user_id):
#     cur=conn.cursor()
#     cur.execute("select p_id from sales where p_id=?",(user_id))
#     sales_p_id=cur.fetchone()
#     if sales_p_id:
#         return jsonify({"message":"p_id is using in sales table so cant delete p_id"})
#     result=cur.execute("delete from inventory where p_id=?",(user_id,))
#     conn.commit()
#     cur.close()
#     if result==0:
#         return jsonify({"message":"data not deleted enter correct id"})
#     return jsonify ({"message":"data delete successfully"})

# #post method of customer

# @app.route("/customer/post", methods=["POST"])
# def customer_post():
#     cur = conn.cursor()
#     customer_name = request.json["customer_name"]
#     customer_pn = request.json["customer_pn"]
#     cur.execute("INSERT INTO customer (customer_name,customer_pn) VALUES (?,?)", (customer_name,customer_pn))
#     # Get the last inserted ID (optional, but useful for knowing which ID was assigned)
#     cur.execute("SELECT @@IDENTITY")
#     last_inserted_id = cur.fetchone()[0]
#     conn.commit()
#     cur.close()
#     return jsonify({"message": "Data added successfully", "customer_id": last_inserted_id}), 201
# #get method of customer

# @app.route("/customer/get/<user_id>",methods=["get"])
# def customer_get(user_id):
#     cur=conn.cursor()
#     result=cur.execute("select * from customer where customer_id=?",(user_id,))
#     data=cur.fetchall()
#     column_name=[disc[0] for disc in cur.description]
#     cur.close()
#     for row in data:
#         data=dict(zip(column_name,row))
#     if result==0:
#         return jsonify({"message":"data not found enter valid id"})
#     return jsonify(data)

# #put method of customer

# @app.route("/customer/put/<user_id>",methods=["put"])
# def customer_put(user_id):
#     cur=conn.cursor()
#     customer_name=request.json["customer_name"]
#     customer_pn=request.json["customer_pn"]
#     result=cur.execute("update customer set customer_name=?,customer_pn=? where customer_id=?",(customer_name,customer_pn,user_id))
#     conn.commit()
#     cur.close()
#     if result==0:
#         return jsonify({"message":"data not updated enter valid id"})
#     return jsonify({"message":"data update successfully"})

# #delete method for customes

# @app.route("/customer/delete/<user_id>",methods=["delete"])
# def customer_delete(user_id):
#     cur=conn.cursor()
#     cur.execute("select customer_id from sales where customer_id=?",(user_id))
#     customer_id=cur.fetchone()
#     if customer_id:
#         return jsonify ({"message":"customes id is using in sales table so cant delete customer id"})
#     result=cur.execute("delete from customer where customer_id=?",(user_id,))
#     conn.commit()
#     cur.close()
#     if result==0:
#         return jsonify({"message":"data not deleted enter valid id"})
#     return jsonify ({"message":"data delete successfully"})


# #post method of sales

# @app.route("/sales/post", methods=["POST"])
# def sales_post():
#     cur = conn.cursor()

#     p_id = request.json["p_id"]
#     customer_id = request.json["customer_id"]
#     units_purchased = request.json["units_purchased"]

#     cur.execute("SELECT quantity FROM inventory WHERE p_id = ?", (p_id,))
#     result = cur.fetchall()

#     if not result:
#         return jsonify({"message": "Product not found"}), 404
    
#     current_stock = result[0][0]  

#     if units_purchased > current_stock:
#         return jsonify({"message": "Insufficient stock"}), 400

#     new_stock = current_stock - units_purchased

#     cur.execute("INSERT INTO sales (p_id, customer_id, units_purchased, stock_after_purchase) VALUES (?, ?, ?, ?)",
#                 (p_id, customer_id, units_purchased, new_stock))

#     cur.execute("UPDATE inventory SET quantity = ? WHERE p_id = ?", (new_stock, p_id))

#     cur.execute("SELECT @@IDENTITY")
#     last_inserted_id = cur.fetchone()[0]

#     conn.commit()
#     cur.close()

#     return jsonify({"message": "Data added successfully", "sales_id": last_inserted_id}), 201

# #get method for sales
# @app.route("/sales/get/<user_id>", methods=["GET"])
# def sales_get(user_id):
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM sales WHERE sales_id = ?", (user_id,))
#     rows = cur.fetchall()
#     column_names = [desc[0] for desc in cur.description]
#     cur.close()

#     if not rows:
#         return jsonify({"message": "Data not found. Enter a valid ID"}), 404

#     # Convert rows to list of dicts
#     data = [dict(zip(column_names, row)) for row in rows]

#     return jsonify(data[0])  # since you're querying by ID, return the first record only



# if (__name__)=="__main__":
#     app.run(host="0.0.0.0", port=8000)




from flask import Flask, request, jsonify
import pyodbc
import os
from azure import identity

app = Flask(__name__)

# Azure SQL Server Configuration
# Use environment variables for security
username = os.environ.get("DB_USERNAME", "rootadmin")
password = os.environ.get("DB_PASSWORD", "P@#sword01")
server = os.environ.get("DB_SERVER", "mysqlserver0001.database.windows.net")
database = os.environ.get("DB_NAME", "testpoc0001")

# Connection string for Azure SQL Server
connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

def get_conn():
    """Get database connection with error handling"""
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        print(f"Database connection error: {e}")
        return None

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
        cur.execute("INSERT INTO category (c_name) OUTPUT INSERTED.c_id VALUES (?)", (c_name,))
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
        cur.execute("SELECT * FROM category WHERE c_id=?", (cat_id,))
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
        cur.execute("UPDATE category SET c_name=? WHERE c_id=?", (c_name, user_id))
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
        cur.execute("SELECT c_id FROM subcategory WHERE c_id=?", (user_id,))
        subcategory_id = cur.fetchone()
        if subcategory_id:
            cur.close()
            conn.close()
            return jsonify({"message": "Category id is used in subcategory table so can't delete it"}), 400
        
        cur.execute("DELETE FROM category WHERE c_id=?", (user_id,))
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
        cur.execute("INSERT INTO subcategory (s_name, c_id) VALUES (?, ?)", (s_name, c_id))
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
        cur.execute("SELECT * FROM subcategory WHERE s_id=?", (user_id,))
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
        cur.execute("UPDATE subcategory SET s_name=? WHERE s_id=?", (s_name, user_id))
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
        cur.execute("SELECT s_id FROM product WHERE s_id=?", (user_id,))
        product_id = cur.fetchone()
        if product_id:
            cur.close()
            conn.close()
            return jsonify({"message": "s_id is used in product table so can't delete it"}), 400
        
        cur.execute("DELETE FROM subcategory WHERE s_id=?", (user_id,))
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
        cur.execute("INSERT INTO product (p_name, p_description, s_id, making_date, batch_no) VALUES (?, ?, ?, ?, ?)", (p_name, p_description, s_id, making_date, batch_no))
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
        cur.execute("SELECT * FROM product WHERE p_id=?", (user_id,))
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
        cur.execute("UPDATE product SET p_name=? WHERE p_id=?", (p_name, user_id))
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
        cur.execute("SELECT p_id FROM inventory WHERE p_id=?", (user_id,))
        inventory_id = cur.fetchone()
        if inventory_id:
            cur.close()
            conn.close()
            return jsonify({"message": "p_id is used in inventory table so can't delete it"}), 400
        
        cur.execute("DELETE FROM product WHERE p_id=?", (user_id,))
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
        cur.execute("INSERT INTO inventory (p_id, p_name, quantity, price) VALUES (?, ?, ?, ?)", (p_id, p_name, quantity, price))
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
        cur.execute("SELECT * FROM inventory WHERE p_id=?", (user_id,))
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
        cur.execute("UPDATE inventory SET p_name=?, quantity=? WHERE p_id=?", (p_name, quantity, user_id))
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
        cur.execute("SELECT p_id FROM sales WHERE p_id=?", (user_id,))
        sales_p_id = cur.fetchone()
        if sales_p_id:
            cur.close()
            conn.close()
            return jsonify({"message": "p_id is used in sales table so can't delete p_id"}), 400
        
        cur.execute("DELETE FROM inventory WHERE p_id=?", (user_id,))
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
        cur.execute("INSERT INTO customer (customer_name, customer_pn) VALUES (?, ?)", (customer_name, customer_pn))
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
        cur.execute("SELECT * FROM customer WHERE customer_id=?", (user_id,))
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
        cur.execute("UPDATE customer SET customer_name=?, customer_pn=? WHERE customer_id=?", (customer_name, customer_pn, user_id))
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
        cur.execute("SELECT customer_id FROM sales WHERE customer_id=?", (user_id,))
        customer_id = cur.fetchone()
        if customer_id:
            cur.close()
            conn.close()
            return jsonify({"message": "Customer id is used in sales table so can't delete customer id"}), 400
        
        cur.execute("DELETE FROM customer WHERE customer_id=?", (user_id,))
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
        
        cur.execute("SELECT quantity FROM inventory WHERE p_id = ?", (p_id,))
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
        cur.execute("INSERT INTO sales (p_id, customer_id, units_purchased, stock_after_purchase) VALUES (?, ?, ?, ?)", (p_id, customer_id, units_purchased, new_stock))
        cur.execute("UPDATE inventory SET quantity = ? WHERE p_id = ?", (new_stock, p_id))
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
        cur.execute("SELECT * FROM sales WHERE sales_id = ?", (user_id,))
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