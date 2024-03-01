from flask import Flask, request, render_template, redirect, jsonify
import os
import mysql.connector as mysql

conn = mysql.connect(
    host = 'localhost',
    user = 'root',
    password = '29012547',
    port =  3306,
    database = 'my_memo'
)

app = Flask(__name__)
templatefolder = os.path.join(os.path.dirname(__file__), "templates")

app.staticfolder = 'static'
app.static_url_path = "/static"

@app.route('/', methods=['GET']) #API
def index():
    cur = conn.reconnect()
    
    sql = "SELECT id_memo, firstname, lastname, email FROM memo"
    cur = conn.cursor()
    cur.execute(sql)
    names = cur.fetchall()
    conn.close()

    return render_template("index.html", names=names)

# @app.route('/product', methods=['GET'])
# def product():
#     item = {
#         "Name" : "Adidas",
#         "Model" : "Ultra Boots",
#         "Price" : 180.0
#     }
#     return item
# @app.route('/news/<id>', methods=['GET']) #Path parameter #GET, you can see at the address bar, but POST cannot
# def news(id):
#     return "Topic no. is" + id

# @app.route('/profile', methods=['GET']) #Get value from GET method
# def profile():
#     name = request.args.get(name)
#     age = request.args.get(age)
#     email = request.args.get(email)
#     return "<B>I am" + name + ', ' + age + " years. This is my" + email + "</B>"

# @app.route('/post-data', methods=['POST'])
# def post_data():
#     name = request.form.get(name)
#     age = request.form.get(age)
#     email = request.form.get(email)
#     return "<B>I am" + name + ', ' + age + " years. This is my" + email + "</B>"

@app.route('/adduser', methods=['GET'])
def add_user():
    return render_template('adduser.html')

@app.route('/adduser_todb', methods=["POST"])
def adduser_todb():
    cur = conn.reconnect()
    
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    
    sql = "INSERT INTO memo(firstname,lastname,email) VALUES(%s,%s,%s)"
    # sql += " "
    data = (firstname,lastname,email)
    
    cur = conn.cursor()
    cur.execute(sql,data)
    conn.commit()
    conn.close()
       
    return index()

@app.route('/delete/<id_memo>',methods=["GET"])
def delete(id_memo):
    cur = conn.reconnect()
    sql = "DELETE FROM memo WHERE id_memo=%s"
    data = (id_memo,)
    
    cur = conn.cursor()
    cur.execute(sql,data)
    conn.commit()
    conn.close()
    
    return index()

@app.route('/edit/<id_memo>',methods=["GET"])
def edit_user(id_memo):
    cur = conn.reconnect()
    sql = "SELECT id_memo, firstname, lastname, email "
    sql += " FROM memo WHERE id_memo = %s"
    data = (id_memo,)
    
    cur = conn.cursor()
    cur.execute(sql,data)
    name = cur.fetchone()
    
    conn.commit()
    conn.close()
    
    return render_template("edit.html", name=name)
    
@app.route('/edituser_todb',methods=["POST"])
def edituser_todb():
    cur = conn.reconnect()

    id_memo = request.form.get('id_memo')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    
    sql = "UPDATE memo SET firstname = %s, lastname = %s, email = %s"
    sql += " WHERE id_memo = %s"
    data = (firstname,lastname,email,id_memo)
    
    cur = conn.cursor()
    cur.execute(sql,data)
    conn.commit()
    conn.close()
    
    return redirect('/')


#Rest API
@app.route ("/getuser/v1/<id_memo>", methods = ['GET'])
def get_user(id_memo):
    cur = conn.reconnect()
    
    sql = "SELECT id_memo, firstname, lastname, email "
    sql += " FROM memo WHERE id_memo = %s ORDER BY firstname"
    data = (id_memo,)
    cur = conn.cursor()
    cur.execute(sql,data)
    records = cur.fetchall()
    conn.close()
    return jsonify(records)

@app.route('/getuser', methods = ["GET"])     
def get_user_all():
    cur = conn.reconnect() 
    
    sql = "SELECT id_memo, firstname, lastname, email "
    sql += " FROM memo ORDER BY firstname" 
    cur = conn.cursor()  
    cur.execute(sql)
    records = cur.fetchall()
    conn.close()
    return jsonify(records)

@app.route('/postuser', methods=["POST"])
def post_user():
    response = request.get_json()
    firstname = response['firstname']
    lastname = response['lastname']
    email = response['email']
    
    cur = conn.reconnect()
    cur = conn.cursor()
    sql = "INSERT INTO memo(firstname, lastname, email) "
    sql += " VALUES(%s,%s,%s)"
    data = (firstname, lastname, email)
    cur.execute(sql,data)
    conn.commit()
    conn.close()
    return redirect('/getuser')


@app.route ('/delete/<email>', methods = ['DELETE'])
def delete_user (email):
    # response = request.get.json()
    # email = response['email']
    cur = conn.reconnect()
    cur = conn.cursor()
    sql = "DELETE FROM memo WHERE email=%s "
    data = (email,)
    cur.execute(sql,data)
    conn.commit()
    conn.close()
    return redirect ('/getuser')

@app.route ('/put_user',methods = ['PUT'])
def put_user():
    response = request.get_json()
    id_memo = response['id_memo']
    firstname = response['firstname']
    lastname = response['lastname']
    email = response['email']
#Update Data
    
    sql = "UPDATE memo SET firstname=%s, lastname=%s, email=%s"
    sql += "WHERE id_memo=%s"
    data = (firstname, lastname, email, id_memo)
    
    cur = conn.reconnect()
    cur = conn.cursor()
    cur.execute(sql,data)
    conn.commit()
    conn.close()
    
    return redirect('/getuser')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)