from flask_restx import Namespace, Resource, fields
from flask import request
from datetime import datetime
from src.models import session
from src.models.tarea_m import Tarea

# Crear namespace para organizar los endpoints de tareas
api = Namespace('tareas', description='Operaciones CRUD para gestión de tareas')

# Modelos para documentación Swagger
tarea_model = api.model('Tarea', {
    'id': fields.Integer(readonly=True, description='ID único de la tarea'),
    'nombre': fields.String(required=True, description='Nombre de la tarea', example='Completar proyecto'),
    'descripcion': fields.String(description='Descripción detallada de la tarea', example='Finalizar el desarrollo del backend'),
    'fecha_creacion': fields.DateTime(readonly=True, description='Fecha de creación automática'),
    'fecha_inicio': fields.DateTime(required=True, description='Fecha de inicio planificada'),
    'fecha_fin': fields.DateTime(description='Fecha de finalización (opcional)'),
    'estado': fields.String(description='Estado actual de la tarea', 
                           enum=['pendiente', 'en_progreso', 'completada'], 
                           default='pendiente',
                           example='pendiente'),
    'fase_id': fields.Integer(required=True, description='ID de la fase asociada', example=1),
    'persona_id': fields.Integer(description='ID de la persona asignada (opcional)', example=1),
    'tablero_id': fields.Integer(required=True, description='ID del tablero/proyecto', example=1)
})

# Modelo para crear/actualizar tarea (sin campos readonly)
tarea_input = api.model('TareaInput', {
    'nombre': fields.String(required=True, description='Nombre de la tarea', example='Completar proyecto'),
    'descripcion': fields.String(description='Descripción detallada de la tarea', example='Finalizar el desarrollo del backend'),
    'fecha_inicio': fields.DateTime(required=True, description='Fecha de inicio planificada', example='2025-01-25T10:00:00'),
    'fecha_fin': fields.DateTime(description='Fecha de finalización (opcional)', example='2025-01-30T18:00:00'),
    'estado': fields.String(description='Estado actual de la tarea', 
                           enum=['pendiente', 'en_progreso', 'completada'], 
                           default='pendiente',
                           example='pendiente'),
    'fase_id': fields.Integer(required=True, description='ID de la fase asociada', example=1),
    'persona_id': fields.Integer(description='ID de la persona asignada (opcional)', example=1),
    'tablero_id': fields.Integer(required=True, description='ID del tablero/proyecto', example=1)
})

# Modelo para respuestas de error
error_model = api.model('Error', {
    'error': fields.String(description='Mensaje de error', example='Datos incompletos'),
    'codigo': fields.Integer(description='Código de error', example=400)
})

# Modelo para respuestas exitosas
success_model = api.model('Success', {
    'mensaje': fields.String(description='Mensaje de éxito', example='Tarea creada exitosamente'),
    'tarea': fields.Nested(tarea_model, description='Datos de la tarea')
})

@api.route('/')
class TareaList(Resource):
    @api.doc('listar_tareas')
    @api.marshal_list_with(tarea_model)
    @api.response(200, 'Lista de tareas obtenida exitosamente')
    @api.response(500, 'Error interno del servidor')
    def get(self):
        """
        Obtener todas las tareas
        
        Retorna una lista completa de todas las tareas registradas en el sistema,
        incluyendo información de fechas, estados y asignaciones.
        """
        try:
            tareas = session.query(Tarea).all()
            return [tarea.to_dict() for tarea in tareas], 200
        except Exception as e:
            api.abort(500, f'Error al obtener tareas: {str(e)}')

    @api.doc('crear_tarea')
    @api.expect(tarea_input, validate=True)
    @api.marshal_with(success_model, code=201)
    @api.response(201, 'Tarea creada exitosamente')
    @api.response(400, 'Datos de entrada inválidos', error_model)
    @api.response(500, 'Error interno del servidor', error_model)
    def post(self):
        """
        Crear una nueva tarea
        
        Crea una nueva tarea en el sistema con los datos proporcionados.
        Los campos requeridos son: nombre, fecha_inicio, fase_id y tablero_id.
        """
        try:
            data = api.payload
            
            # Validaciones adicionales
            if not data.get('nombre'):
                api.abort(400, 'El campo nombre es requerido')
            
            if not data.get('fecha_inicio'):
                api.abort(400, 'El campo fecha_inicio es requerido')
            
            # Convertir fecha_inicio de string a datetime si es necesario
            fecha_inicio = data.get('fecha_inicio')
            if isinstance(fecha_inicio, str):
                try:
                    fecha_inicio = datetime.fromisoformat(fecha_inicio.replace('Z', '+00:00'))
                except ValueError:
                    api.abort(400, 'Formato de fecha_inicio inválido. Use formato ISO 8601')
            
            # Convertir fecha_fin si se proporciona
            fecha_fin = data.get('fecha_fin')
            if fecha_fin and isinstance(fecha_fin, str):
                try:
                    fecha_fin = datetime.fromisoformat(fecha_fin.replace('Z', '+00:00'))
                except ValueError:
                    api.abort(400, 'Formato de fecha_fin inválido. Use formato ISO 8601')
            
            # Crear nueva tarea
            nueva_tarea = Tarea(
                nombre=data['nombre'],
                descripcion=data.get('descripcion', ''),
                fecha_inicio=fecha_inicio,
                estado=data.get('estado', 'pendiente')
            )
            
            # Asignar campos requeridos
            nueva_tarea.fase_id = data.get('fase_id', 1)
            nueva_tarea.tablero_id = data.get('tablero_id', 1)
            nueva_tarea.persona_id = data.get('persona_id')
            nueva_tarea.fecha_fin = fecha_fin
            
            # Guardar en base de datos
            session.add(nueva_tarea)
            session.commit()
            session.refresh(nueva_tarea)
            
            return {
                'mensaje': 'Tarea creada exitosamente',
                'tarea': nueva_tarea.to_dict()
            }, 201
            
        except Exception as e:
            session.rollback()
            api.abort(500, f'Error al crear la tarea: {str(e)}')

@api.route('/<int:tarea_id>')
@api.param('tarea_id', 'ID único de la tarea')
class TareaResource(Resource):
    @api.doc('obtener_tarea')
    @api.marshal_with(tarea_model)
    @api.response(200, 'Tarea obtenida exitosamente')
    @api.response(404, 'Tarea no encontrada', error_model)
    @api.response(500, 'Error interno del servidor', error_model)
    def get(self, tarea_id):
        """
        Obtener una tarea específica por ID
        
        Retorna los detalles completos de una tarea específica
        identificada por su ID único.
        """
        try:
            tarea = session.query(Tarea).filter_by(id=tarea_id).first()
            if not tarea:
                api.abort(404, f'Tarea con ID {tarea_id} no encontrada')
            
            return tarea.to_dict(), 200
            
        except Exception as e:
            api.abort(500, f'Error al obtener la tarea: {str(e)}')

    @api.doc('actualizar_tarea')
    @api.expect(tarea_input, validate=True)
    @api.marshal_with(success_model)
    @api.response(200, 'Tarea actualizada exitosamente')
    @api.response(404, 'Tarea no encontrada', error_model)
    @api.response(400, 'Datos de entrada inválidos', error_model)
    @api.response(500, 'Error interno del servidor', error_model)
    def put(self, tarea_id):
        """
        Actualizar una tarea existente
        
        Actualiza todos los campos de una tarea existente.
        Todos los campos en el payload reemplazarán los valores actuales.
        """
        try:
            tarea = session.query(Tarea).filter_by(id=tarea_id).first()
            if not tarea:
                api.abort(404, f'Tarea con ID {tarea_id} no encontrada')
            
            data = api.payload
            
            # Actualizar campos
            if 'nombre' in data:
                tarea.nombre = data['nombre']
            if 'descripcion' in data:
                tarea.descripcion = data['descripcion']
            if 'estado' in data:
                tarea.estado = data['estado']
            if 'fase_id' in data:
                tarea.fase_id = data['fase_id']
            if 'tablero_id' in data:
                tarea.tablero_id = data['tablero_id']
            if 'persona_id' in data:
                tarea.persona_id = data['persona_id']
            
            # Actualizar fechas si se proporcionan
            if 'fecha_inicio' in data:
                fecha_inicio = data['fecha_inicio']
                if isinstance(fecha_inicio, str):
                    fecha_inicio = datetime.fromisoformat(fecha_inicio.replace('Z', '+00:00'))
                tarea.fecha_inicio = fecha_inicio
            
            if 'fecha_fin' in data:
                fecha_fin = data['fecha_fin']
                if fecha_fin and isinstance(fecha_fin, str):
                    fecha_fin = datetime.fromisoformat(fecha_fin.replace('Z', '+00:00'))
                tarea.fecha_fin = fecha_fin
            
            session.commit()
            session.refresh(tarea)
            
            return {
                'mensaje': 'Tarea actualizada exitosamente',
                'tarea': tarea.to_dict()
            }, 200
            
        except Exception as e:
            session.rollback()
            api.abort(500, f'Error al actualizar la tarea: {str(e)}')

    @api.doc('eliminar_tarea')
    @api.response(200, 'Tarea eliminada exitosamente')
    @api.response(404, 'Tarea no encontrada', error_model)
    @api.response(500, 'Error interno del servidor', error_model)
    def delete(self, tarea_id):
        """
        Eliminar una tarea
        
        Elimina permanentemente una tarea del sistema.
        Esta acción no se puede deshacer.
        """
        try:
            tarea = session.query(Tarea).filter_by(id=tarea_id).first()
            if not tarea:
                api.abort(404, f'Tarea con ID {tarea_id} no encontrada')
            
            session.delete(tarea)
            session.commit()
            
            return {'mensaje': f'Tarea {tarea_id} eliminada exitosamente'}, 200
            
        except Exception as e:
            session.rollback()
            api.abort(500, f'Error al eliminar la tarea: {str(e)}')

@api.route('/estado/<string:estado>')
@api.param('estado', 'Estado de las tareas a filtrar (pendiente, en_progreso, completada)')
class TareasPorEstado(Resource):
    @api.doc('listar_tareas_por_estado')
    @api.marshal_list_with(tarea_model)
    @api.response(200, 'Tareas filtradas por estado')
    @api.response(500, 'Error interno del servidor')
    def get(self, estado):
        """
        Obtener tareas filtradas por estado
        
        Retorna todas las tareas que coincidan con el estado especificado.
        Estados válidos: pendiente, en_progreso, completada
        """
        try:
            tareas = session.query(Tarea).filter_by(estado=estado).all()
            return [tarea.to_dict() for tarea in tareas], 200
        except Exception as e:
            api.abort(500, f'Error al filtrar tareas: {str(e)}')
