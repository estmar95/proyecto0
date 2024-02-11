from typing import Any
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from datetime import datetime
import enum

db = SQLAlchemy()

categoria_tarea = db.Table('categoria_tarea',\
    db.Column('categoria_id', db.Integer, db.ForeignKey('categoria.id'), primary_key=True),
    db.Column('tarea_id', db.Integer, db.ForeignKey('tarea.id'), primary_key=True))

class Estado(enum.Enum):
    SIN_EMPEZAR = 1
    EMPEZADA = 2
    FINALIZADA = 3

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(128))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_finalizacion = db.Column(db.DateTime, nullable=True)  # Permitir que fecha_finalizacion sea nullable
    estado = db.Column(db.Enum(Estado))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    descripcion = db.Column(db.String(255))
    tareas = db.relationship('Tarea', secondary=categoria_tarea, backref='categorias')

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_de_usuario = db.Column(db.String(128))
    contrasena = db.Column(db.String(128))
    tareas = db.relationship('Tarea', cascade='all, delete, delete-orphan', backref='usuario', lazy=True)

class EnumEDiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {'llave':value.name, 'valor': value.value}

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

class CategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        include_relationships = True
        load_instance = True

class TareaSchema(SQLAlchemyAutoSchema):
    estado = EnumEDiccionario(attribute='estado')
    class Meta:
        model = Tarea
        include_relationships = True
        load_instance = True



