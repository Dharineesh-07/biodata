from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

#Connecting to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    return "Hello"

#GET

@app.route('/item/<key>', methods=['GET'])
def get_item(key):
    value = r.get(key)
    if value:
        return jsonify({key: value.decode('utf-8')}), 200
    else:
        return jsonify({'error': 'Key not found'}), 404

#POST

@app.route('/item', methods=['POST'])
def create_item():
    data = request.json
    key = data.get('key')
    value = data.get('value')
    if key and value:
        r.set(key, value)
        return jsonify({'message': 'Item created'}), 201
    else:
        return jsonify({'error': 'Invalid input'}), 400

#PUT

@app.route('/item/<key>', methods=['PUT'])
def update_item(key):
    data = request.json
    value = data.get('value')
    if r.exists(key):
        r.set(key, value)
        return jsonify({'message': 'Item updated'}), 200
    else:
        return jsonify({'error': 'Key not found'}), 404

#DELETE

@app.route('/item/<key>', methods=['DELETE'])
def delete_item(key):
    if r.exists(key):
        r.delete(key)
        return jsonify({'message': 'Item deleted'}), 200
    else:
        return jsonify({'error': 'Key not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
