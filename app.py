from flask import Flask, request, jsonify
from flask.views import MethodView

app = Flask(__name__)

# Aquí almacenaremos los directorios para este ejemplo
directories = []

class StatusView(MethodView):
    def get(self):
        return jsonify('pong')

class DirectoryView(MethodView):
    def get(self, directory_id=None):
        if directory_id is None:
            return jsonify({
                "count": len(directories),
                "next": "link a siguiente página",
                "previous": "link a página previa",
                "results": directories
            })
        else:
            for directory in directories:
                if directory['id'] == directory_id:
                    return jsonify(directory)
            return jsonify({'error': 'Directory not found'}), 404
        
    def patch(self, directory_id):
        update_data = request.get_json()
        for directory in directories:
            if directory['id'] == directory_id:
                directory.update(update_data)
                return jsonify(directory)
        return jsonify({'error': 'Directory not found'}), 404

    def delete(self, directory_id):
        for index, directory in enumerate(directories):
            if directory['id'] == directory_id:
                del directories[index]
                return jsonify({'success': True})
        return jsonify({'error': 'Directory not found'}), 404
    def post(self):
            new_directory = request.get_json()
            new_directory['id'] = len(directories) + 1
            directories.append(new_directory)
            return jsonify(new_directory), 201

    def put(self, directory_id):
        update_data = request.get_json()
        for directory in directories:
            if directory['id'] == directory_id:
                directory.update(update_data)
                return jsonify(directory)
        return jsonify({'error': 'Directory not found'}), 404

app.add_url_rule('/status/', view_func=StatusView.as_view('status'))
app.add_url_rule('/directories/', view_func=DirectoryView.as_view('directories'))
app.add_url_rule('/directories/<int:directory_id>/', view_func=DirectoryView.as_view('directory'))

if __name__ == '__main__':
    app.run(debug=True)