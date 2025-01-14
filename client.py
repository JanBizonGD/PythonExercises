#/usr/bin/python3
import requests
import argparse
import json
import os

base = 'http://localhost:5000'
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--instruction')
    parser.add_argument('-n', '--order-number')
    parser.add_argument('-p', '--pizza')


    args = parser.parse_args()

    if args.instruction:
        instruction = str.lower(args.instruction)
        if instruction == 'menu':
            res = requests.get(base + '/menu', headers=headers)
            print(res.text)
        if instruction == 'order':
            if args.pizza:
                pizzas = args.pizza.split()
                payload = {
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
            print(res.text)

os.environ['TOKEN'] = "Bearer Token"