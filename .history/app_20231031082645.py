from flask import Flask, current_app, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Directorios(db.Model):
    __tablename__ = 'directorios'

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(30), unique=True, nullable=False)
    emails = db.Column(db.ARRAY(db.String(50)), unique=True, nullable=False) 

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'emails': self.emails
        }

with app.app_context():
    db.create_all()

@app.route('/status/', methods=['GET'])
def get_status():
    return 'pong'

@app.route('/directories', methods=['POST']) 
def create_directory():
    try:
        data = request.get_json()
        directorio = Directorios(name=data['name'], emails=data['emails'])
        db.session.add(directorio)
        db.session.commit()
        return make_response(jsonify({'message': 'directorio creado'}), 201)
    except Exception:
        return make_response(jsonify({'message': 'error creando el directorio'}), 500)

@app.route('/directories', methods=['GET'])
def get_directories():
    try:
        directorios = Directorios.query.all()
        if len(directorios):
            return make_response(jsonify({
                'count': len(directorios),
                'next': "link a siguiente página",
                'previous': "link a página previa",
                'results': [directorio.serialize() for directorio in directorios]
            }), 200)
        return make_response(jsonify({'message': 'directorios no encontrados'}), 404)     
    except Exception:
        return make_response(jsonify({'message': 'error obteniendo a los directorios'}), 500)

@app.route('/directories/<int:id>', methods=['GET'])
def get_directory(id):
    try:
        directorio = Directorios.query.get(id)
        return make_response(jsonify({'directorio': directorio.serialize()}), 200)     
    except Exception:
        return make_response(jsonify({'message': 'error obteniendo al directorio'}), 500)

@app.route('/directories/<int:id>', methods=['PUT'])
def update_directory(id):
    try:
        directorio = Directorios.query.get(id)
        if directorio:
            data = request.get_json()
            directorio.name = data['name']
            directorio.emails = data['emails']
            db.session.commit()
            return make_response(jsonify({'message': 'directorio actualizado'}), 200)
        return make_response(jsonify({'message': 'directorio no encontrado'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error actualizando el directorio'}), 500)

@app.route('/directories/<int:id>', methods=['PATCH'])
def partial_update_directory(id):
    try:
        directorio = Directorios.query.get(id)
        if directorio:
            data = request.get_json()
            if 'name' in data:
                directorio.name = data['name']
            if 'emails' in data:
                directorio.emails = data['emails']
            db.session.commit()
            return make_response(jsonify({'message': 'directorio actualizado'}), 200)
        return make_response(jsonify({'message': 'directorio no encontrado'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error actualizando el directorio'}), 500)

@app.route('/directories/<int:id>', methods=['DELETE'])
def delete_directory(id):
    try:
        directorio = Directorios.query.get(id)
        if directorio:
            db.session.delete(directorio)
            db.session.commit()
            return make_response(jsonify({'message': 'directorio eliminado'}), 200)
        return make_response(jsonify({'message': 'directorio no encontrado'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error eliminando el directorio'}), 500)
