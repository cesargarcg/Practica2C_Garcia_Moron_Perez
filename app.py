from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cnp2_user:my_cool_secret_2@postgres-db/cnp2_database'
db = SQLAlchemy(app)

class Directory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    emails = db.Column(ARRAY(db.String), nullable=False)

@app.route('/status/')
def get_status():
    return 'pong'

@app.route('/directories/')
def get_directories():
    directories = Directory.query.all()
    directory_list = []
    for directory in directories:
        directory_data = {
            'id': directory.id,
            'name': directory.name,
            'emails': directory.emails
        }
        directory_list.append(directory_data)

    return jsonify({
        "count": len(directory_list),
        "next": 'link a siguiente página',
        "previous": 'link a página previa',
        "results": directory_list
    })

@app.route('/directories/', methods=['POST'])
def create_directory():
    new_directory = Directory(**request.json)
    db.session.add(new_directory)
    db.session.commit()

    return jsonify({
        'id': new_directory.id,
        'name': new_directory.name,
        'emails': new_directory.emails
    }), 201

@app.route('/directories/<int:id>')
def get_directory(id):
    directory = Directory.query.get(id)
    if directory:
        directory_data = {
            'id': directory.id,
            'name': directory.name,
            'emails': directory.emails
        }
        return jsonify(directory_data)
    return jsonify({'error': 'Object not found'}), 404

@app.route('/directories/<int:id>', methods=['PUT'])
def update_directory(id):
    data = request.get_json()
    directory = Directory.query.get(id)
    if directory:
        directory.name = data['name']
        directory.emails = data['emails']
        db.session.commit()
        return jsonify({
            'id': directory.id,
            'name': directory.name,
            'emails': directory.emails
        })
    return jsonify({'error': 'Object not found'}), 404

@app.route('/directories/<int:id>', methods=['PATCH'])
def partial_update_directory(id):
    data = request.get_json()
    directory = Directory.query.get(id)
    if directory:
        if 'name' in data:
            directory.name = data['name']
        if 'emails' in data:
            directory.emails = data['emails']
        db.session.commit()
        return jsonify({
            'id': directory.id,
            'name': directory.name,
            'emails': directory.emails
        })
    return jsonify({'error': 'Object not found'}), 404

@app.route('/directories/<int:id>', methods=['DELETE'])
def delete_directory(id):
    directory = Directory.query.get(id)
    if directory:
        db.session.delete(directory)
        db.session.commit()
        return jsonify({'message': 'Object deleted'})
    return jsonify({'error': 'Object not found'}), 404

if __name__ == '__main__':
    app.run()