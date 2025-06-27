from flask import Flask, request, jsonify
import pyodbc
from azure import identity
from dotenv import load_dotenv
import os

load_dotenv()  

app = Flask(__name__)

db_server = os.getenv("DB_SERVER")
db_name = os.getenv("DB_NAME")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")

connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server=tcp:{db_server},1433;"
    f"Database={db_name};"
    f"Uid={db_username};"
    f"Pwd={db_password};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

def get_conn():

    conn = pyodbc.connect(connection_string)
    return conn

conn = get_conn()

@app.route('/')
def index():
    return "Flask Api Running!"



@app.route("/category/post", methods=["POST"])
def category_post():
    
        cur = conn.cursor()
        c_name = request.json["c_name"]

        cur.execute("INSERT INTO category (c_name) OUTPUT INSERTED.c_id VALUES (?)", (c_name,))

        cur.execute("SELECT @@IDENTITY")
        last_inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return jsonify({"message": "Data added successfully", "c_id": last_inserted_id}), 201

@app.route("/")
def hello():
    return "Hello your api is Running"




#get method of category

@app.route("/category/get/<cat_id>",methods=["get"])
def category_get(cat_id):
    cur=conn.cursor()
    result=cur.execute("select * from category where c_id=?",(cat_id,))
    data=cur.fetchall()
    column_name=[disc[0] for disc in cur.description]
    cur.close()
    for row in data:
        data=dict(zip(column_name,row))
    if result==0:
        return jsonify({"message":"data not found due to invalid category id"})
    return jsonify(data)

#put method of category

@app.route("/category/put/<user_id>",methods=["put"])
def category_put(user_id):
    cur=conn.cursor()
    c_name=request.json["c_name"]
    result=cur.execute("update category set c_name=%s where c_id=%s ",(c_name,user_id))
    print(result)
    conn.commit()
    if result==0:
        return jsonify ({"message":"data not updated"})
    cur.close()
    return jsonify({"message":"data update successfully"})

#delete method of category

@app.route("/category/delete/<user_id>",methods=["delete"])
def category_delete(user_id):
    cur=conn.cursor()
    cur.execute("select c_id from Subcategory where c_id=?",(user_id))
    Subcategory_id=cur.fetchone()
    if Subcategory_id:
        cur.close()
        return jsonify({"message":"category id uses in Subcategory table so can't delete it"})
    cur.execute("delete from category where c_id=?",(user_id))
    conn.commit()
    if cur.rowcount==0:
        cur.close()
        return jsonify({"message":"data not delete"})
    cur.close()
    return jsonify ({"message":"data delete successfully"})

#post method of Subcategory

@app.route("/subcategory/post",methods=["post"])
def subcategory_post():
    cur=conn.cursor()
    S_name=request.json["S_name"]
    c_id=request.json["c_id"]
    cur.execute("insert into Subcategory (S_name,c_id) values (?,?)",(S_name,c_id))
    # Get the last inserted ID (optional, but useful for knowing which ID was assigned)
    cur.execute("SELECT @@IDENTITY")
    last_inserted_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({"message": "Data added successfully", "s_id": last_inserted_id}), 201

#get method of Subcategory

@app.route("/subcategory/get/<user_id>",methods=["get"])
def subcategory_get(user_id):
    cur=conn.cursor()
    result=cur.execute("select * from Subcategory where s_id=?",(user_id))
    data=cur.fetchall()
    column_name=[disc[0] for disc in cur.description]
    cur.close()
    for row in data:
        data=dict(zip(column_name,row))
    if result==0:
        return jsonify({"message":"data not found due to invalid id"})
    return jsonify(data)

#put method of Subcategory

@app.route("/subcategory/put/<user_id>",methods=["put"])
def subcategory_put(user_id):
    cur=conn.cursor()
    s_name=request.json["s_name"]
    result=cur.execute("update Subcategory set s_name=%s where s_id=%s",(s_name,user_id))
    conn.commit()
    cur.close()
    if result==0:
        return jsonify({"message":"data not updated"})
    return jsonify({"message":"data update successfully"})

#delete method of Subcategory

@app.route("/subcategory/delete/<user_id>",methods=["delete"])
def subcategory_delete(user_id):
    cur=conn.cursor()
    cur.execute("select s_id from product where s_id=?",(user_id))
    product_id=cur.fetchone()
    if product_id:
        return jsonify ({"message":"s_id is using in product table so can't delete it"})
    result=cur.execute("delete from Subcategory where s_id=?",(user_id))
    conn.commit()
    cur.close()
    if result==0:
        return jsonify({"message":"enter valid id"})
    return jsonify ({"message":"data delete successfully"})

#post method of product

@app.route("/product/post",methods=["post"])
def product_post():
    cur=conn.cursor()
    p_name=request.json["p_name"]
    p_description=request.json["p_description"]
    s_id=request.json["s_id"]
    making_date=request.json["making_date"]
    batch_no=request.json["batch_no"]
    cur.execute("insert into product (p_name,p_description,s_id,making_date,batch_no) values (?,?,?,?,?)",(p_name,p_description,s_id,making_date,batch_no))
    # Get the last inserted ID (optional, but useful for knowing which ID was assigned)
    cur.execute("SELECT @@IDENTITY")
    last_inserted_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({"message": "Data added successfully", "p_id": last_inserted_id}), 201

#get method of product

@app.route("/product/get/<user_id>",methods=["get"])
def product_get(user_id):
    cur=conn.cursor()
    result=cur.execute("select * from product where p_id=?",(user_id))
    data=cur.fetchall()
    column_name=[disc[0] for disc in cur.description]
    cur.close()
    for row in data:
        data=dict(zip(column_name,row))
    if result==0:
        return jsonify({"message":"data not found enter valid id"})
    return jsonify(data)

#put method of product

@app.route("/product/put/<user_id>",methods=["put"])
def product_put(user_id):
    cur=conn.cursor()
    p_name=request.json["p_name"]
    result=cur.execute("update product set p_name=? where p_id=?",(p_name,user_id))
    conn.commit()
    cur.close()
    if result==0:
        return jsonify({"message":"data not updated"})
    return jsonify({"message":"data update successfully"})

#delete method of product

@app.route("/product/delete/<user_id>",methods=["delete"])
def product_delete(user_id):
    cur=conn.cursor()
    cur.execute("select p_id from inventory where p_id=?",(user_id))
    invenory_id=cur.fetchone()
    if invenory_id:
        return jsonify({"message":"p_id is using in inventory table so can't delete it"})
    result=cur.execute("delete from product where p_id=?",(user_id))
    conn.commit()
    cur.close()
    if result==0:
        return jsonify({"message":"data not deleted enter valid id"})
    return jsonify ({"message":"data delete s+uccessfully"})

#post method for inventory

@app.route("/inventory/post",methods=["post"])
def inventory_post():
    cur=conn.cursor()
    p_id=request.json["p_id"]
    p_name=request.json["p_name"]
    quantity=request.json["quantity"]
    price=request.json["price"]
    cur.execute("insert into inventory (p_id,p_name,quantity,price) values (?,?,?,?)",(p_id,p_name,quantity,price))
    # Get the last inserted ID (optional, but useful for knowing which ID was assigned)
    cur.execute("SELECT @@IDENTITY")
    last_inserted_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({"message": "Data added successfully", "i_id": last_inserted_id}), 201
#get method of inventory

@app.route("/inventory/get/<user_id>",methods=["get"])
def inventory_get(user_id):
    cur=conn.cursor()
    result=cur.execute("select * from inventory where p_id=?",(user_id))
    data=cur.fetchall()
    column_name=[disc[0] for disc in cur.description]
    cur.close()
    for row in data:
        data=dict(zip(column_name,row))
    if result==0:
        return jsonify({"messsage":"data not found enter correct id"})
    return jsonify(data)

#put method of inventory

@app.route("/inventory/put/<user_id>",methods=["put"])
def inventory_put(user_id):
    cur=conn.cursor()
    p_name=request.json["p_name"]
    quantity=request.json["quantity"]
    result=cur.execute("update inventory set p_name=?,quantity=? where p_id=?",(p_name,quantity,user_id))
    conn.commit()
    cur.close()
    if result==0:
        return jsonify({"message":"data not updated"})
    return jsonify({"message":"data update successfully"})

#delete method of inventory

@app.route("/inventory/delete/<user_id>",methods=["delete"])
def inventory_delete(user_id):
    cur=conn.cursor()
    cur.execute("select p_id from sales where p_id=?",(user_id))
    sales_p_id=cur.fetchone()
    if sales_p_id:
        return jsonify({"message":"p_id is using in sales table so cant delete p_id"})
    result=cur.execute("delete from inventory where p_id=?",(user_id,))
    conn.commit()
    cur.close()
    if result==0:
        return jsonify({"message":"data not deleted enter correct id"})
    return jsonify ({"message":"data delete successfully"})

#post method of customer

@app.route("/customer/post", methods=["POST"])
def customer_post():
    cur = conn.cursor()
    customer_name = request.json["customer_name"]
    customer_pn = request.json["customer_pn"]
    cur.execute("INSERT INTO customer (customer_name,customer_pn) VALUES (?,?)", (customer_name,customer_pn))
    # Get the last inserted ID (optional, but useful for knowing which ID was assigned)
    cur.execute("SELECT @@IDENTITY")
    last_inserted_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({"message": "Data added successfully", "customer_id": last_inserted_id}), 201
#get method of customer

@app.route("/customer/get/<user_id>",methods=["get"])
def customer_get(user_id):
    cur=conn.cursor()
    result=cur.execute("select * from customer where customer_id=?",(user_id,))
    data=cur.fetchall()
    column_name=[disc[0] for disc in cur.description]
    cur.close()
    for row in data:
        data=dict(zip(column_name,row))
    if result==0:
        return jsonify({"message":"data not found enter valid id"})
    return jsonify(data)

#put method of customer

@app.route("/customer/put/<user_id>",methods=["put"])
def customer_put(user_id):
    cur=conn.cursor()
    customer_name=request.json["customer_name"]
    customer_pn=request.json["customer_pn"]
    result=cur.execute("update customer set customer_name=?,customer_pn=? where customer_id=?",(customer_name,customer_pn,user_id))
    conn.commit()
    cur.close()
    if result==0:
        return jsonify({"message":"data not updated enter valid id"})
    return jsonify({"message":"data update successfully"})

#delete method for customes

@app.route("/customer/delete/<user_id>",methods=["delete"])
def customer_delete(user_id):
    cur=conn.cursor()
    cur.execute("select customer_id from sales where customer_id=?",(user_id))
    customer_id=cur.fetchone()
    if customer_id:
        return jsonify ({"message":"customes id is using in sales table so cant delete customer id"})
    result=cur.execute("delete from customer where customer_id=?",(user_id,))
    conn.commit()
    cur.close()
    if result==0:
        return jsonify({"message":"data not deleted enter valid id"})
    return jsonify ({"message":"data delete successfully"})


#post method of sales

@app.route("/sales/post", methods=["POST"])
def sales_post():
    cur = conn.cursor()

    p_id = request.json["p_id"]
    customer_id = request.json["customer_id"]
    units_purchased = request.json["units_purchased"]

    cur.execute("SELECT quantity FROM inventory WHERE p_id = ?", (p_id,))
    result = cur.fetchall()

    if not result:
        return jsonify({"message": "Product not found"}), 404
    
    current_stock = result[0][0]  

    if units_purchased > current_stock:
        return jsonify({"message": "Insufficient stock"}), 400

    new_stock = current_stock - units_purchased

    cur.execute("INSERT INTO sales (p_id, customer_id, units_purchased, stock_after_purchase) VALUES (?, ?, ?, ?)",
                (p_id, customer_id, units_purchased, new_stock))

    cur.execute("UPDATE inventory SET quantity = ? WHERE p_id = ?", (new_stock, p_id))

    cur.execute("SELECT @@IDENTITY")
    last_inserted_id = cur.fetchone()[0]

    conn.commit()
    cur.close()

    return jsonify({"message": "Data added successfully", "sales_id": last_inserted_id}), 201

#get method for sales
@app.route("/sales/get/<user_id>", methods=["GET"])
def sales_get(user_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales WHERE sales_id = ?", (user_id,))
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    cur.close()

    if not rows:
        return jsonify({"message": "Data not found. Enter a valid ID"}), 404

    # Convert rows to list of dicts
    data = [dict(zip(column_names, row)) for row in rows]

    return jsonify(data[0])  # since you're querying by ID, return the first record only

if __name__ == '__main__':
    app.run(debug = True)



