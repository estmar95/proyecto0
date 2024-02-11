from flaskr import create_app
from .modelos import db, Usuario, Categoria, Tarea, Estado
from .modelos.modelos import TareaSchema, CategoriaSchema, UsuarioSchema
from datetime import datetime
from flask_restful import Api
from .vistas import vistaTareas, vistaTarea, VistaCategoria, VistaCategorias, VistaUsuario, VistaUsuarios, VistaSignIn, VistaTareasUsuario
from flask_jwt_extended import JWTManager
from flask import send_from_directory, jsonify, request

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(vistaTareas, '/tareas')
api.add_resource(vistaTarea, '/tarea/<int:id_tarea>')
api.add_resource(VistaUsuarios, '/usuarios')
api.add_resource(VistaUsuario, '/usuario/<int:id_usuario>')
api.add_resource(VistaCategorias, '/categorias')
api.add_resource(VistaCategoria, '/categoria/<int:id_categoria>')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaTareasUsuario, '/usuarios/<int:id_usuario>/tareas')

jwt = JWTManager(app)

# Configurar la ruta estática para la carpeta 'frontend'
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    if path == '':
        return send_from_directory('frontend', 'index.html')
    else:
        # Si se solicita un archivo estático, servirlo desde la carpeta frontend
        return send_from_directory('frontend', path)

# Agregar una regla para servir la carpeta estática
@app.route('/frontend/<path:path>')
def serve_static_frontend(path):
    return send_from_directory('frontend', path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
