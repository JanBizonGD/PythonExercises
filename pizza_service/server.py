#/usr/lib/python
# Backend
from flask import Flask, request, render_template
import sqlite3, json
import uuid

# init_db.py - for initialisation of database
# schema.sql - description of databases structure

# Launch backend:
# flask --app ./server.py run --host=0.0.0.0
# default port : 5000


class Pizza():
    def __init__(self, *args):
        if len(args) == 4:
            self.id = args[0]
            self.name = args[1]
            self.ingredients = args[2].copy()
            self.price = args[3]
 
class Order():
    def __init__(self, pizza_ids, status):
        self.pizzas = pizza_ids
        self.status = status
    def changeStatus(self, status):
        self.status = status


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Welcome. To see menu go to /menu. If you would like to place order visit /order. </p>"

@app.get("/menu")
def list_menu():
    conn = get_db_connection()
    curr = conn.cursor()
    res = curr.execute('SELECT * FROM pizza;').fetchall()
    conn.close()
    pizzas = []
    for p in res:
        ingred = ''.join(p['ingredients']).strip('[').strip(']').strip('\'').split(', ')
        pizzas.append(Pizza(p['id'], p['nameText'], ingred, p['price']))
    return render_template('menu.html', data=pizzas)

@app.post("/menu")
def add_pizza():
    if not check_auth(request.headers):
        return {}, 401
    payload = request.json
    pizza = Pizza(0, payload['name'], payload['ingriedients'], payload['price'])
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute('INSERT INTO pizza (nameText, ingredients, price) VALUES (?, ?, ?);', (pizza.name, f'{pizza.ingredients}', pizza.price))
    conn.commit()
    conn.close()
    return {}

@app.delete("/menu/<int:pizza_id>")
def delete_pizza(pizza_id):
    if not check_auth(request.headers):
        return {}, 401
    conn = get_db_connection()
    conn.execute('DELETE FROM pizza WHERE (?) = id', (pizza_id, ))
    conn.commit()
    conn.close()
    return {}

@app.post("/order")
def place_order():
    check_auth(request.headers)
    user_id = request.json['user_id']
    order = Order(request.json['pizzas'], "order placed")
    try:
        conn = get_db_connection()
        curr = conn.cursor()
        curr.execute('INSERT INTO orderTab(user_id, pizzas, statusText) VALUES (?, ?, ?);', (user_id, f'{order.pizzas}', order.status))
        conn.commit()
        id = curr.lastrowid
        conn.close()
    except sqlite3.Error as err:
        return {"message" : f"Error while inserting order: {err}"}
    return { "order_index": id }

@app.get("/order/<int:order_id>")
def check_status(order_id):
    check_auth(request.headers)
    try:
        conn = get_db_connection()
        curr = conn.cursor()
        res = curr.execute('SELECT user_id, pizzas, statusText FROM orderTab WHERE id = (?);', (order_id, )).fetchone()
        conn.close()
    except sqlite3.Error as err:
        return {"message" : f"Error while inserting order: {err}"}
    return {"status" : res['statusText']}

@app.delete("/order/<int:order_id>")
def cancel_order(order_id):
    status = check_status(order_id)["status"]
    if status != "ready_to_be_delivered" or check_auth(request.headers):
        try:
            conn = get_db_connection()
            curr = conn.cursor()
            print('Cancel')
            curr.execute('UPDATE orderTab SET  statusText = (?) WHERE id = (?);', ("canceled", order_id))
            conn.commit()
            conn.close()
        except sqlite3.Error as err:
            return {"message" : f"Error while inserting order: {err}"}
        return check_status(order_id)


@app.post("/login")
def auth():
    payload = request.json
    if payload['login'] and payload['password']:
        if compere_credentials(payload['login'], payload['password']):
            conn = get_db_connection()
            cur = conn.cursor()
            res = cur.execute('SELECT bearerToken FROM login WHERE loginText = (?)', (payload['login'], )).fetchone()
            conn.commit()
            conn.close()
            print(res['bearerToken'])
            return json.dumps({'auth' : True , 'token': res['bearerToken']})
    return {'auth' : False}

@app.post("/register")
def register():
    payload = request.json
    if payload['login'] and payload['password']:
        if not compere_credentials(payload['login'], payload['password']):
            token = str(uuid.uuid4())
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO login(loginText, passwordText, administrator, bearerToken) VALUES (?, ?, ?, ?)',\
                         (payload['login'], payload['password'], False, token))
            conn.commit()
            conn.close()
            return json.dumps({'auth' : True , 'token': token})
    return {'auth' : False}


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def compere_credentials(login, password):
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM login').fetchall()
    conn.close()
    for post in posts:
        if login == post['loginText']:
            if password == post['passwordText']:
                return True
    return False

def compare_token(token):
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM login').fetchall()
    conn.close()
    for post in posts:
        if post['bearerToken'] == token:
            return True
    return False

def check_auth(headers):
    try:
        if headers.get('Authorization'):
            bearer_token = headers.get('Authorization').split()[2]
            print(bearer_token)
            conn = get_db_connection()
            posts = conn.execute('SELECT administrator FROM login WHERE bearerToken = (?)', (bearer_token, )).fetchone()
            conn.close()
            return posts['administrator']
    except TypeError as err:
        print(f'No authorization: {err}')
        return {'message' : 'No authorization'}, 401
    return False
