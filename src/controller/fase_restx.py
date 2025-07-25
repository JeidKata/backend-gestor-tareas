from flask_restx import Namespace, Resource, fields
from flask import request
from src.models.fase_m import Fase
from src.models import session

# Namespace para Fase
fase_ns = Namespace(
    'fase', 
    description='Operaciones CRUD para fases'
)

# Modelos para Swagger
fase_model = fase_ns.model('Fase', {
    'nombre': fields.String(required=True, description="Nombre"),
    'id': fields.Integer(description='ID único')
})

fase_input = fase_ns.model('FaseInput', {
    'nombre': fields.String(required=True, description="Nombre")
})

fase_response = fase_ns.model('FaseResponse', {
    'mensaje': fields.String(description='Mensaje de respuesta'),
    'fase': fields.Nested(fase_model)
})

@fase_ns.route('/')
class FaseList(Resource):
    @fase_ns.doc('listar_fases')
    @fase_ns.marshal_list_with(fase_model)
    def get(self):
        """Obtener todas las fases"""
        try:
            fases = Fase.obtener_fases()
            return fases, 200
        except Exception as e:
            fase_ns.abort(500, f"Error interno: {str(e)}")

    @fase_ns.doc('crear_fase')
    @fase_ns.expect(fase_input)
    @fase_ns.marshal_with(fase_response, code=201)
    def post(self):
        """Crear una nueva fase"""
        try:
            data = request.get_json()
            fase_nuevo = Fase.crear_fase(**data)
            return {
                'mensaje': 'Fase creada exitosamente',
                'fase': fase_nuevo
            }, 201
        except Exception as e:
            session.rollback()
            fase_ns.abort(500, f"Error al crear fase: {str(e)}")

@fase_ns.route('/<int:id>')
@fase_ns.param('id', 'ID de la fase')
class FaseResource(Resource):
    @fase_ns.doc('obtener_fase')
    @fase_ns.marshal_with(fase_model)
    def get(self, id):
        """Obtener una fase específica"""
        try:
            fase = Fase.obtener_fase_por_id(id)
            if fase:
                return fase, 200
            else:
                fase_ns.abort(404, "Fase no encontrada")
        except Exception as e:
            fase_ns.abort(500, f"Error interno: {str(e)}")

    @fase_ns.doc('actualizar_fase')
    @fase_ns.expect(fase_input)
    @fase_ns.marshal_with(fase_response)
    def put(self, id):
        """Actualizar una fase"""
        try:
            data = request.get_json()
            fase_actualizada = Fase.actualizar_fase(id, **data)
            if fase_actualizada:
                return {
                    'mensaje': 'Fase actualizada exitosamente',
                    'fase': fase_actualizada
                }, 200
            else:
                fase_ns.abort(404, "Fase no encontrada")
        except Exception as e:
            session.rollback()
            fase_ns.abort(500, f"Error al actualizar fase: {str(e)}")

    @fase_ns.doc('eliminar_fase')
    def delete(self, id):
        """Eliminar una fase"""
        try:
            if Fase.eliminar_fase(id):
                return {'mensaje': 'Fase eliminada exitosamente'}, 200
            else:
                fase_ns.abort(404, "Fase no encontrada")
        except Exception as e:
            session.rollback()
            fase_ns.abort(500, f"Error al eliminar fase: {str(e)}")
