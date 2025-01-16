#/usr/bin/python3
# Frontend
import requests
import argparse
import json
import os

# python client.py -i cancel -n 2
# python client.py -i status -n 2
# python client.py -i order -p "[8, 9]"
# python client.py -i menu
# python client.py -i menu -p my_pizza "[abc, efg]" 30
# python client.py -i menu -p 8
# python client.py -i login
# python client.py -i register

base = 'http://localhost:5000'
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
if os.path.exists('.auth'):
    token = ""
    with open('.auth', 'r', encoding='utf-8') as f:
        token = f.readline()
    if token:
        headers['Authorization'] = token

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--instruction')
    parser.add_argument('-n', '--order-number')
    parser.add_argument('-p', '--pizza', nargs='+')


    args = parser.parse_args()

    if args.instruction:
        instruction = str.lower(args.instruction)
        if instruction == 'menu':
            if args.pizza:
                pizza_args = args.pizza
                if len(pizza_args) != 3 and len(pizza_args) != 1:
                    print('Wrong number of arguments for registering new pizza')
                elif len(pizza_args) == 3:
                    ingred = pizza_args[1].strip('[').strip(']').split(', ')
                    payload = {
                        'name' : pizza_args[0],
                        'ingriedients': ingred,
                        'price' : pizza_args[2]
                    }
                    res = requests.post(base + '/menu', data=json.dumps(payload), headers=headers)
                    if res.status_code < 300:
                        print('===== Posted successfully ======')
                    else:
                        print('===== Error during posting new pizza =======')
                        print('Pizza name should be unique')
                else:
                    pizza_id = int(args.pizza[0])
                    res = requests.delete(base + f'/menu/{pizza_id}', headers=headers)
                    if res.status_code > 200:
                        print('Error during deleting pizza')
            res = requests.get(base + '/menu', headers=headers)
            print(res.text)
        if instruction == 'order':
            if args.pizza:
                pizzas = args.pizza
                payload = {
                    "user_id": 0,
                    "pizzas": pizzas,
                    "message": "Place order"
                    }
                res = requests.post(base + '/order', json.dumps(payload), headers=headers)
                print(res.text)
        if instruction == 'cancel':
            if args.order_number:
                res = requests.delete(base + f'/order/{args.order_number}', headers=headers)
                print(res.text)
            else :
                print("Specify index of order with -n.")
        if instruction == 'status':
            if args.order_number:
                res = requests.get(base + f'/order/{args.order_number}', headers=headers)
                print(res.text)
            else :
                print("Specify index of order with -n.")
        if instruction == 'login':
            login = input('Login:')
            password = input('Password:')
            payload = {
                'login' : login,
                'password' : password
            }
            res = requests.post(base + '/login', json.dumps(payload), headers=headers)
            if 'token' in res.json():
                token =  "Bearer Token " + res.json()['token']
                with open('.auth', 'w+', encoding='utf-8') as f:
                    f.write(token)
                print('Bearer Token assigned.')
                print(token)
            else:
                print('Authorization unsuccessfull! Try again.')
        if instruction == 'register':
            login = input('Login:')
            password = input('Password:')
            payload = {
                'login' : login,
                'password' : password
            }
            res = requests.post(base + '/register', json.dumps(payload), headers=headers)
            if res.json()['auth']:
                print('======= Registered successfully =======')
            else :
                print('Error during registration.')
