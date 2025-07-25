from flask_restx import Namespace, Resource, fields
from flask import request
from src.models.persona_m import Persona
from src.models import session

# Namespace para Persona
persona_ns = Namespace(
    'persona', 
    description='Operaciones CRUD para personas'
)

# Modelos para Swagger
persona_model = persona_ns.model('Persona', {
    'nombre': fields.String(required=True, description="Nombre"),
    'correo': fields.String(required=True, description="Correo"),
    'password': fields.String(required=True, description="Password"),
    'id': fields.Integer(description='ID único')
})

persona_input = persona_ns.model('PersonaInput', {
    'nombre': fields.String(required=True, description="Nombre"),
    'correo': fields.String(required=True, description="Correo"),
    'password': fields.String(required=True, description="Password")
})

persona_response = persona_ns.model('PersonaResponse', {
    'mensaje': fields.String(description='Mensaje de respuesta'),
    'persona': fields.Nested(persona_model)
})

@persona_ns.route('/')
class PersonaList(Resource):
    @persona_ns.doc('listar_personas')
    @persona_ns.marshal_list_with(persona_model)
    def get(self):
        """Obtener todas las personas"""
        try:
            personas = Persona.obtener_personas()
            return personas, 200
        except Exception as e:
            persona_ns.abort(500, f"Error interno: {str(e)}")

    @persona_ns.doc('crear_persona')
    @persona_ns.expect(persona_input)
    @persona_ns.marshal_with(persona_response, code=201)
    def post(self):
        """Crear una nueva persona"""
        try:
            data = request.get_json()
            persona_nuevo = Persona.crear_persona(**data)
            return {
                'mensaje': 'Persona creada exitosamente',
                'persona': persona_nuevo
            }, 201
        except Exception as e:
            session.rollback()
            persona_ns.abort(500, f"Error al crear persona: {str(e)}")

@persona_ns.route('/<int:id>')
@persona_ns.param('id', 'ID de la persona')
class PersonaResource(Resource):
    @persona_ns.doc('obtener_persona')
    @persona_ns.marshal_with(persona_model)
    def get(self, id):
        """Obtener una persona específica"""
        try:
            persona = Persona.obtener_persona_por_id(id)
            if persona:
                return persona, 200
            else:
                persona_ns.abort(404, "Persona no encontrada")
        except Exception as e:
            persona_ns.abort(500, f"Error interno: {str(e)}")

    @persona_ns.doc('actualizar_persona')
    @persona_ns.expect(persona_input)
    @persona_ns.marshal_with(persona_response)
    def put(self, id):
        """Actualizar una persona"""
        try:
            data = request.get_json()
            persona_actualizada = Persona.actualizar_persona(id, **data)
            if persona_actualizada:
                return {
                    'mensaje': 'Persona actualizada exitosamente',
                    'persona': persona_actualizada
                }, 200
            else:
                persona_ns.abort(404, "Persona no encontrada")
        except Exception as e:
            session.rollback()
            persona_ns.abort(500, f"Error al actualizar persona: {str(e)}")

    @persona_ns.doc('eliminar_persona')
    def delete(self, id):
        """Eliminar una persona"""
        try:
            if Persona.eliminar_persona(id):
                return {'mensaje': 'Persona eliminada exitosamente'}, 200
            else:
                persona_ns.abort(404, "Persona no encontrada")
        except Exception as e:
            session.rollback()
            persona_ns.abort(500, f"Error al eliminar persona: {str(e)}")
