from flask_restful import Resource
from ..modelos import db, Tarea, Usuario, Categoria
from ..modelos.modelos import TareaSchema, UsuarioSchema, CategoriaSchema
from flask import request
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token


tarea_schema = TareaSchema()
usuario_schema = UsuarioSchema()
categoria_schema = CategoriaSchema()

class vistaTareas(Resource):

    def get(self):
        return [tarea_schema.dump(tarea) for tarea in Tarea.query.all()]

    def post(self):
        fecha_creacion = datetime.fromisoformat(request.json['fecha_creacion'])
        fecha_finalizacion = request.json.get('fecha_finalizacion')  # Obtener la fecha_finalizacion si está presente
        nueva_tarea = Tarea(
            texto=request.json['texto'],
            fecha_creacion=fecha_creacion,
            fecha_finalizacion=fecha_finalizacion,
            estado=request.json['estado']
        )
        db.session.add(nueva_tarea)
        db.session.commit()
        return tarea_schema.dump(nueva_tarea)

    
class vistaTarea(Resource):

    def get(self, id_tarea):
        return tarea_schema.dump(Tarea.query.get_or_404(id_tarea))
    
    def put(self, id_tarea):
        tarea = Tarea.query.get_or_404(id_tarea)
        tarea.texto = request.json.get('texto', tarea.texto)
        tarea.fecha_creacion = request.json.get('fecha_creacion', tarea.fecha_creacion)
        tarea.fecha_finalizacion = request.json.get('fecha_finalizacion', tarea.fecha_finalizacion)
        tarea.estado = request.json.get('estado', tarea.estado)
        db.session.commit()
        return tarea_schema.dump(tarea)
    
    def delete(self, id_tarea):
        tarea = Tarea.query.get_or_404(id_tarea)
        db.session.delete(tarea)
        db.session.commit()
        return 'Operacion exitosa', 204

class VistaUsuarios(Resource):

    def get(self):
        return [usuario_schema.dump(usuario) for usuario in Usuario.query.all()]
    
    def post(self):
        nuevo_usuario = Usuario(
            nombre_de_usuario=request.json['nombre_de_usuario'],
            contrasena=request.json['contrasena'],
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return usuario_schema.dump(nuevo_usuario)
    
class VistaUsuario(Resource):

    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return usuario_schema.dump(usuario)
    
    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.nombre_de_usuario = request.json.get('nombre_de_usuario', usuario.nombre_de_usuario)
        usuario.contrasena = request.json.get('contrasena', usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)
    
    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return 'Operacion exitosa', 204
    
class VistaSignIn(Resource):
    def post(self):
        nuevo_usuario = Usuario(nombre_de_usuario=request.json['nombre_de_usuario'],contrasena=request.json['contrasena'])
        token_de_acceso = create_access_token(identity=request.json['nombre_de_usuario'])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {'Mensaje': 'Usuario creado exitosamente', 'token_de_acceso': token_de_acceso}
    
    def put(self, id_usuario):
                usuario = Usuario.query.get_or_404(id_usuario)
                usuario.nombre_de_usuario = request.json.get('nombre_de_usuario', usuario.nombre_de_usuario)
                usuario.contrasena = request.json.get('contrasena', usuario.contrasena)
                db.session.commit()
                return usuario_schema.dump(usuario)


class VistaTareasUsuario(Resource):

    @jwt_required()
    def post(self, id_usuario):
        fecha_creacion = datetime.fromisoformat(request.json['fecha_creacion'])
        nueva_tarea = Tarea(texto = request.json['texto'], fecha_creacion = fecha_creacion, fecha_finalizacion = request.json['fecha_finalizacion'], estado = request.json['estado'])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.tareas.append(nueva_tarea)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene una tarea con dicho texto'

    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [tarea_schema.dump(ta) for ta in usuario.tareas]


class VistaCategorias(Resource):

    def get(self):
        return [categoria_schema.dump(categoria) for categoria in Categoria.query.all()]
    
    def post(self):
        nueva_categoria = Categoria(
            nombre=request.json['nombre'],
            descripcion=request.json['descripcion']
        )
        db.session.add(nueva_categoria)
        db.session.commit()
        return categoria_schema.dump(nueva_categoria)
    
class VistaCategoria(Resource):

    def get(self, id_categoria):
        categoria = Categoria.query.get_or_404(id_categoria)
        return categoria_schema.dump(categoria)
    
    def put(self, id_categoria):
        categoria = Categoria.query.get_or_404(id_categoria)
        categoria.nombre = request.json.get('nombre', categoria.nombre)
        categoria.descripcion = request.json.get('descripcion', categoria.descripcion)
        db.session.commit()
        return categoria_schema.dump(categoria)
    
    def delete(self, id_categoria):
        categoria = Categoria.query.get_or_404(id_categoria)
        db.session.delete(categoria)
        db.session.commit()
        return 'Operacion exitosa', 204