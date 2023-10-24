from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista de objetos
objects = []
# Variable para llevar el seguimiento del último ID asignado
last_id = 0

# Endpoint: GET /status/
@app.route('/status/')
def get_status():
    return 'pong'

# Endpoint: GET /directories/
@app.route('/directories/')
def get_directories():
    return jsonify({
        "count": len(objects),
        "next": 'link a siguiente página',
        "previous": 'link a página previa',
        "results": objects
    })

# Endpoint: POST /directories/
@app.route('/directories/', methods=['POST'])
def create_directory():
    global last_id
    data = request.get_json()
    # Asignar un nuevo ID incremental
    last_id += 1
    data['id'] = last_id
    objects.append(data)
    return jsonify(data), 201

# Endpoint: GET /directories/{id}
@app.route('/directories/<int:id>')
def get_directory(id):
    directory = next((obj for obj in objects if obj['id'] == id), None)
    if directory:
        return jsonify(directory)
    return jsonify({'error': 'Object not found'}), 404

# Endpoint: PUT /directories/{id}
@app.route('/directories/<int:id>', methods=['PUT'])
def update_directory(id):
    data = request.get_json()
    directory = next((obj for obj in objects if obj['id'] == id), None)
    if directory:
        directory.update(data)
        return jsonify(directory)
    return jsonify({'error': 'Object not found'}), 404

# Endpoint: PATCH /directories/{id}
@app.route('/directories/<int:id>', methods=['PATCH'])
def partial_update_directory(id):
    data = request.get_json()
    directory = next((obj for obj in objects if obj['id'] == id), None)
    if directory:
        directory.update(data)
        return jsonify(directory)
    return jsonify({'error': 'Object not found'}), 404

# Endpoint: DELETE /directories/{id}
@app.route('/directories/<int:id>', methods=['DELETE'])
def delete_directory(id):
    directory = next((obj for obj in objects if obj['id'] == id), None)
    if directory:
        objects.remove(directory)
        return jsonify({'message': 'Object deleted'})
    return jsonify({'error': 'Object not found'}), 404

if __name__ == '__main__':
    app.run()