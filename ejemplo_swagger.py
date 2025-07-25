from flask import Flask
from flask_restx import Api, Resource, fields
from datetime import datetime

app = Flask(__name__)
api = Api(app, doc='/docs/', title='Gestor de Tareas API', description='API para gestión de tareas')

# Namespace para organizar endpoints
ns_tareas = api.namespace('tareas', description='Operaciones de tareas')

# Modelos para documentación
tarea_model = api.model('Tarea', {
    'id': fields.Integer(description='ID único de la tarea'),
    'titulo': fields.String(required=True, description='Título de la tarea'),
    'descripcion': fields.String(description='Descripción de la tarea'),
    'fecha_creacion': fields.DateTime(description='Fecha de creación'),
    'estado': fields.String(description='Estado de la tarea')
})

tarea_input = api.model('TareaInput', {
    'titulo': fields.String(required=True, description='Título de la tarea'),
    'descripcion': fields.String(description='Descripción de la tarea')
})

@ns_tareas.route('/')
class TareaList(Resource):
    @ns_tareas.doc('listar_tareas')
    @ns_tareas.marshal_list_with(tarea_model)
    def get(self):
        """Obtener todas las tareas"""
        tareas_ejemplo = [
            {
                'id': 1,
                'titulo': 'Tarea de ejemplo 1',
                'descripcion': 'Esta es una tarea de ejemplo',
                'fecha_creacion': datetime.now(),
                'estado': 'pendiente'
            },
            {
                'id': 2,
                'titulo': 'Tarea de ejemplo 2',
                'descripcion': 'Otra tarea de ejemplo',
                'fecha_creacion': datetime.now(),
                'estado': 'pendiente'
            }
        ]
        return tareas_ejemplo

    @ns_tareas.doc('crear_tarea')
    @ns_tareas.expect(tarea_input)
    @ns_tareas.marshal_with(tarea_model, code=201)
    def post(self):
        """Crear una nueva tarea"""
        data = api.payload
        nueva_tarea = {
            'id': 3,
            'titulo': data['titulo'],
            'descripcion': data.get('descripcion', ''),
            'fecha_creacion': datetime.now(),
            'estado': 'pendiente'
        }
        return nueva_tarea, 201

@ns_tareas.route('/<int:id>')
@ns_tareas.param('id', 'ID de la tarea')
class Tarea(Resource):
    @ns_tareas.doc('obtener_tarea')
    @ns_tareas.marshal_with(tarea_model)
    def get(self, id):
        """Obtener una tarea específica"""
        tarea = {
            'id': id,
            'titulo': f'Tarea {id}',
            'descripcion': 'Descripción de ejemplo',
            'fecha_creacion': datetime.now(),
            'estado': 'pendiente'
        }
        return tarea

    @ns_tareas.doc('actualizar_tarea')
    @ns_tareas.expect(tarea_input)
    @ns_tareas.marshal_with(tarea_model)
    def put(self, id):
        """Actualizar una tarea"""
        data = api.payload
        tarea_actualizada = {
            'id': id,
            'titulo': data['titulo'],
            'descripcion': data.get('descripcion', ''),
            'fecha_creacion': datetime.now(),
            'estado': 'pendiente'
        }
        return tarea_actualizada

    @ns_tareas.doc('eliminar_tarea')
    def delete(self, id):
        """Eliminar una tarea"""
        return {'mensaje': f'Tarea {id} eliminada exitosamente'}, 200

if __name__ == '__main__':
    app.run(debug=True)
