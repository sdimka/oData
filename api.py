from flask import Flask, request, jsonify
from flask_api import status
from flask_cors import CORS
import json

from datetime import datetime

from order import order

app = Flask(__name__)
CORS(app)

user_list = [
    {'sd': '12345'},
    {'td': '54321'},
    {'aau': 'LVL86x'}
]

orders = []


def genFakePrders():
    for i in range(30):
        orders.append(order(i, '29.06.2020', 4501 + i, 'Иванов Иван Иванович', 150, True, 1))
    for i in range(25):
        orders.append(order(i, '30.06.2020', 4601 + i, 'Иванов Иван Иванович', 100, True, 1))
    for i in range(25):
        orders.append(order(i, '3.07.2020', 4701 + i, 'Иванов Иван Иванович', 100, True, 1))


@app.route('/get/', methods=['GET'])
def get_list():
    res = ''
    for a in (10, 1):

        res += f'{a } {a + 3}' + '\n'
        print(res)
    return res


@app.route('/getOrders/', methods=['GET'])
def get_order_list():
    # today = (datetime.today() + '')[0-]
    start_date = datetime.strptime(request.args.get('startDate', default='', type=str), '%d/%m/%Y')
    end_date = datetime.strptime(request.args.get('endDate', default='', type=str), '%d/%m/%Y')
    print(start_date)
    res = json.dumps([order.__dict__ for order in orders])
    return res


@app.route('/user', methods=['POST'])
def get_user():
    data = request.get_json()
    if 'login' in data and 'password' in data:
        for a in user_list:
            if data['login'] in a and a[data['login']] == data['password']:
                print('Ok login!')
                response = jsonify({'some': 'data'})
                return response
    response = jsonify({'some': 'data'})
    return 'Record not found', status.HTTP_401_UNAUTHORIZED


if __name__ == '__main__':
    genFakePrders()
    app.run(host='0.0.0.0', debug=True)
