from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb+srv://dharineesh:12345@cluster0.srfg0w5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['mydb']
collection = db['mycollection']

@app.route('/')
def home():
    return "Hello"

#INSERT

@app.route('/insert', methods=['POST'])
def insert():
    data = request.json
    result = collection.insert_one(data)
    return jsonify(str(result.inserted_id)), 201

#GET

@app.route('/get', methods=['GET'])
def get():
    query = request.args.to_dict()
    documents = list(collection.find(query))
    for document in documents:
        document['_id'] = str(document['_id'])  
    return jsonify(documents), 200

#PUT

@app.route('/update/<id>', methods=['PUT'])
def update(id):
    data = request.json
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.modified_count > 0:
        return jsonify({'message': 'Document updated successfully'}), 200
    else:
        return jsonify({'message': 'No document found or nothing to update'}), 404

#DELETE

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Document deleted successfully'}), 200
    else:
        return jsonify({'message': 'No document found'}), 404

if __name__ == "__main__":
    app.run(debug=True)
