#/usr/lib/python
from flask import Flask, request
import sqlite3, json
import uuid

# flask --app ./server.py run --host=0.0.0.0
# default port : 5000

# curl --request POST \
#   --url localhost:5000/order \
#   --header 'Accept: application/json' \
#   --header 'Authorization: Bearer Tt.2Iv46AZKynGS5hz60l32clVu-jbGpEg2DIv8cCNTdIesZN57fRjDsP8JF4a1yih20uhHM65F9BqQ4lojJ5qRtfNZN..lBrwpRD6Fet0HivpcYEucXw88jjcAK7p4h' \
#   --header 'Content-Type: application/json' \
#   --data '{"message": "Place order"}'


def incrementId():
    id = 0    
    while True:
        yield id
        id +=1
class Pizza():
    index_gen = incrementId()
    def __init__(self, *args):
        if len(args) == 1:
            pizza_id = args[0]
            self.id = next(Pizza.index_gen)
            self.name = pizzas[pizza_id].name
            self.ingredients = pizzas[pizza_id].ingredients
            self.price = pizzas[pizza_id].price
        elif len(args) == 3:
            name = args[0]
            ingredients = args[1]
            price = args[2]
            self.id = next(Pizza.index_gen)
            self.name = name
            self.ingredients = ingredients.copy()
            self.price = price
 
class Order():
    index_gen = incrementId()
    def __init__(self, pizza_ids, status):
        self.id = next(Order.index_gen)
        self.pizzas = list((map(lambda pizza_id : Pizza(int(pizza_id)), pizza_ids)))
        self.status = status
        self.totalPrice = self.calcPrice()
    def calcPrice(self):
        sum = 0
        for pizza in self.pizzas:
            sum += pizza.price
        return sum
    def changeStatus(self, status):
        self.status = status

class User():
    def __init__(self):
        self.name = ""
        self.password = ""
        self.admin = False
        self.token = ""


# pizzas
pizzas = [
    Pizza("Margaritta", ["sos pomidorowy", "cheese"], 20),
    Pizza("Capricciosa", ["sos pomidorowy", "mozzarella", "szynka", "pieczarki"], 25),
    Pizza("Pepperoni", ["sos pomidorowy", "mozzarella", "pepperoni"], 27),
    Pizza("Hawaiian", ["sos pomidorowy", "mozzarella", "szynka", "ananas"], 25),
    Pizza("Vegetariana", ["sos pomidorowy", "mozzarella", "papryka", "pieczarki", "cebula", "oliwki", "kukurydza"], 35),
    Pizza("Carbonara", ["sos smietanowy", "mozzarella", "boczek", "jajko", "parmezan"], 30)
    ]

orders = []

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Welcome. To see menu go to /menu. If you would like to place order visit /order. </p>"

@app.get("/menu")
def list_menu():
    body = """
        <section>
            <h2>Our Pizzas</h2>
                <div class="menu-category">"""
    body += ''.join(map(lambda pizza :
    f"""
                <div class="item">
                    <span class="item-id">{pizza.id}</span>
                    <span class="item-name">{pizza.name}</span>
                    <span class="item-price">${pizza.price}</span>
                    <span class="item-ingred">{pizza.ingredients}</span>
                </div>
    """, pizzas))
    body += """
            </div>
        </section>"""
    return body

@app.post("/order")
def place_order():
    print(request.json['pizzas'])
    orders.append(Order(request.json['pizzas'], "order placed"))
    print(orders[0].pizzas[0].name)
    return { "order_index": orders[-1].id }

@app.get("/order/<int:order_id>")
def check_status(order_id):
    filtered_out = list(filter(lambda order : order.id == order_id, orders))
    print(filtered_out[0].status)
    if len(filtered_out) > 0:
        return filtered_out[0].status
    return {}

@app.delete("/order/<int:order_id>")
def cancel_order(order_id):
    if check_status(order_id) != "ready_to_be_delivered":
        filtered_out = list(filter(lambda order : order.id == order_id, orders))
        orders[orders.index(filtered_out[0])].status = "canceled"
    return orders[orders.index(filtered_out[0])].status


bearer_token = "" # secure storage
@app.post("/login")
def auth():
    payload = request.json
    if payload['login'] and payload['password']:
        if compere_credentials(payload['login'], payload['password']):
            return json.dumps({'auth' : True , 'token': str(uuid.uuid4())})
    return {'auth' : False}

@app.post("/menu")
def add_pizza():
    pass

@app.delete("/menu/{pizza_id}")
def delete_pizza():
    pass

# @app.delete("/order/{order_id}")
# def cancel_order():
#     #with force - only admin 
#     return "<p>Hello, World!</p>"

# register with securing user credentials


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

