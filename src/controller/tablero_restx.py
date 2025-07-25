from flask_restx import Namespace, Resource, fields
from flask import request
from src.models.tablero_m import Tablero
from src.models import session

# Namespace para Tablero
tablero_ns = Namespace(
    'tablero', 
    description='Operaciones CRUD para tableros'
)

# Modelos para Swagger
tablero_model = tablero_ns.model('Tablero', {
    'nombre': fields.String(required=True, description="Nombre"),
    'descripcion': fields.String(description="Descripcion"),
    'fecha_creacion': fields.DateTime(description="Fecha Creacion"),
    'fecha_entrega': fields.DateTime(description="Fecha Entrega"),
    'estado': fields.String(description="Estado"),
    'id': fields.Integer(description='ID único')
})

tablero_input = tablero_ns.model('TableroInput', {
    'nombre': fields.String(required=True, description="Nombre"),
    'descripcion': fields.String(description="Descripcion"),
    'fecha_creacion': fields.DateTime(description="Fecha Creacion"),
    'fecha_entrega': fields.DateTime(description="Fecha Entrega"),
    'estado': fields.String(description="Estado")
})

tablero_response = tablero_ns.model('TableroResponse', {
    'mensaje': fields.String(description='Mensaje de respuesta'),
    'tablero': fields.Nested(tablero_model)
})

@tablero_ns.route('/')
class TableroList(Resource):
    @tablero_ns.doc('listar_tableros')
    @tablero_ns.marshal_list_with(tablero_model)
    def get(self):
        """Obtener todas las tableros"""
        try:
            tableros = Tablero.obtener_tableros()
            return tableros, 200
        except Exception as e:
            tablero_ns.abort(500, f"Error interno: {str(e)}")

    @tablero_ns.doc('crear_tablero')
    @tablero_ns.expect(tablero_input)
    @tablero_ns.marshal_with(tablero_response, code=201)
    def post(self):
        """Crear una nueva tablero"""
        try:
            data = request.get_json()
            tablero_nuevo = Tablero.crear_tablero(**data)
            return {
                'mensaje': 'Tablero creada exitosamente',
                'tablero': tablero_nuevo
            }, 201
        except Exception as e:
            session.rollback()
            tablero_ns.abort(500, f"Error al crear tablero: {str(e)}")

@tablero_ns.route('/<int:id>')
@tablero_ns.param('id', 'ID de la tablero')
class TableroResource(Resource):
    @tablero_ns.doc('obtener_tablero')
    @tablero_ns.marshal_with(tablero_model)
    def get(self, id):
        """Obtener una tablero específica"""
        try:
            tablero = Tablero.obtener_tablero_por_id(id)
            if tablero:
                return tablero, 200
            else:
                tablero_ns.abort(404, "Tablero no encontrada")
        except Exception as e:
            tablero_ns.abort(500, f"Error interno: {str(e)}")

    @tablero_ns.doc('actualizar_tablero')
    @tablero_ns.expect(tablero_input)
    @tablero_ns.marshal_with(tablero_response)
    def put(self, id):
        """Actualizar una tablero"""
        try:
            data = request.get_json()
            tablero_actualizada = Tablero.actualizar_tablero(id, **data)
            if tablero_actualizada:
                return {
                    'mensaje': 'Tablero actualizada exitosamente',
                    'tablero': tablero_actualizada
                }, 200
            else:
                tablero_ns.abort(404, "Tablero no encontrada")
        except Exception as e:
            session.rollback()
            tablero_ns.abort(500, f"Error al actualizar tablero: {str(e)}")

    @tablero_ns.doc('eliminar_tablero')
    def delete(self, id):
        """Eliminar una tablero"""
        try:
            if Tablero.eliminar_tablero(id):
                return {'mensaje': 'Tablero eliminada exitosamente'}, 200
            else:
                tablero_ns.abort(404, "Tablero no encontrada")
        except Exception as e:
            session.rollback()
            tablero_ns.abort(500, f"Error al eliminar tablero: {str(e)}")
