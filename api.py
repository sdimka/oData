from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/get/', methods=['GET'])
def get_list():
    res = ''
    for a in (10, 1):

        res += f'{a } {a + 3}' + '\n'
        print(res)
    return res


@app.route('/user', methods=['POST'])
def get_user():
    un = request.args.get('user')
    print(request.args)
    response = jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
