from flask import Flask, request, jsonify
from flask_api import status
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

user_list = [
    {'sd': '12345'},
    {'td': '54321'}
]


@app.route('/get/', methods=['GET'])
def get_list():
    res = ''
    for a in (10, 1):

        res += f'{a } {a + 3}' + '\n'
        print(res)
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
    app.run(host='0.0.0.0', debug=True)
