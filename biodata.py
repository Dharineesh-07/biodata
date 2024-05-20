from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:biodata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Biodata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    department = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Biodata {self.name}>'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'department': self.department
        }

with app.app_context():
    db.create_all()

@app.route('/submit', methods=['POST'])
def submit_biodata():
    data = request.get_json()
    new_biodata = Biodata(
        name=data['name'],
        age=data['age'],
        email=data['email'],
        department=data['department']
    )
    db.session.add(new_biodata)
    db.session.commit()
    return jsonify(new_biodata.serialize()), 201

@app.route('/biodata', methods=['GET'])
def get_biodata():
    biodata_list = Biodata.query.all()
    return jsonify([biodata.serialize() for biodata in biodata_list]), 200

if __name__ == '__main__':
    app.run(debug=True)
