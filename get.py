from flask import Flask, request

app = Flask(__name__)

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name')
    if name:
        return f'Hello, {name}!'
    else:
        return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
