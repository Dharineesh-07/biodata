from flask import Flask, request, jsonify
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select

app = Flask(__name__)

# Database connection
db_url = "sqlite:///D:\\database.db"
engine = create_engine(db_url)
metadata = MetaData()

# Define the table schema
my_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False),
    Column('age', Integer, nullable=False))

# Create table if it doesn't exist
metadata.create_all(engine, checkfirst=True)

@app.route('/create_data', methods=['POST'])
def create_data():
    # Get the raw data from the request
    raw_data = request.get_json()

    if raw_data:
        # Extract data fields from the raw data
        name = raw_data.get('name')
        age = raw_data.get('age')

        # Construct an insert query
        insert_query = my_table.insert().values(name=name, age=age)

        # Execute the insert query
        with engine.connect() as connection:
            result = connection.execute(insert_query)
            new_id = result.inserted_primary_key[0]
            return f'Data created with ID: {new_id}', 201
    else:
        return 'No data provided', 400

@app.route('/get_data', methods=['GET'])
def get_all_data():
    # Construct a select query to fetch all data
    query = select([my_table])

    # Execute the query
    with engine.connect() as connection:
        result = connection.execute(query)
        data = [dict(row) for row in result]
        return jsonify(data), 200

@app.route('/get_data/<int:id>', methods=['GET'])
def get_data_by_id(id):
    # Construct a select query to fetch data based on ID
    query = select([my_table]).where(my_table.c.id == id)

    # Execute the query
    with engine.connect() as connection:
        result = connection.execute(query)
        data = [dict(row) for row in result]
        if data:
            return jsonify(data), 200
        else:
            return 'No data found for the provided ID', 404

@app.route('/update_data/<int:id>', methods=['PUT'])
def update_data(id):
    # Get the raw data from the request
    raw_data = request.get_json()

    if raw_data:
        # Extract data fields from the raw data
        name = raw_data.get('name')
        age = raw_data.get('age')

        # Construct an update query
        update_query = my_table.update().where(my_table.c.id == id).values(name=name, age=age)

        # Execute the update query
        with engine.connect() as connection:
            connection.execute(update_query)
            return f'Data with ID {id} updated successfully', 200
    else:
        return 'No data provided', 400

@app.route('/delete_data/<int:id>', methods=['DELETE'])
def delete_data(id):
    # Construct a delete query to delete data based on ID
    delete_query = my_table.delete().where(my_table.c.id == id)

    # Execute the delete query
    with engine.connect() as connection:
        connection.execute(delete_query)
        return f'Data with ID {id} deleted successfully', 200

if __name__ == '__main__':
    app.run(debug=True)
