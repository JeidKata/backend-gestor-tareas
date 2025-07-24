from app import app
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_controller import FlaskController
from datetime import datetime

@app.route('/')
def home():
    return "<h1>¡Aplicación Flask corriendo correctamente!</h1>"

class ClientesController(FlaskController):
    @app.route("/tareas", methods=['GET', 'POST'])
    def manejar_tareas():
        if request.method == 'POST':
            # Crear tarea
            data = request.get_json()
            if not data or 'titulo' not in data or 'descripcion' not in data:
                return jsonify({'error': 'Datos incompletos'}), 400

            tarea = {
                'titulo': data['titulo'],
                'descripcion': data['descripcion'],
                'fecha_creacion': datetime.utcnow().isoformat()
            }

            # Aquí deberías guardar la tarea en la base de datos
            # Por ahora, solo devolvemos la tarea creada como ejemplo

            return jsonify({'mensaje': 'Tarea creada exitosamente', 'tarea': tarea}), 201
        
        elif request.method == 'GET':
            # Obtener tareas
            # Por ahora devolvemos tareas de ejemplo
            tareas_ejemplo = [
                {
                    'id': 1,
                    'titulo': 'Tarea de ejemplo 1',
                    'descripcion': 'Esta es una tarea de ejemplo',
                    'fecha_creacion': datetime.now().isoformat()
                },
                {
                    'id': 2,
                    'titulo': 'Tarea de ejemplo 2',
                    'descripcion': 'Otra tarea de ejemplo',
                    'fecha_creacion': datetime.now().isoformat()
                }
            ]
            
            return jsonify({
                'mensaje': 'Tareas obtenidas exitosamente',
                'tareas': tareas_ejemplo,
                'total': len(tareas_ejemplo)
            }), 200
        
    @app.route("/tareas/<int:id>g", methods=['GET'])
    def manejar_tarea(id):
        # Aquí deberías buscar la tarea por ID en la base de datos
        # Por ahora devolvemos una tarea de ejemplo
        tarea_ejemplo = {
            'id': id,
            'titulo': f'Tarea de ejemplo {id}',
            'descripcion': 'Esta es una tarea de ejemplo',
            'fecha_creacion': datetime.now().isoformat()
        }
        
        if tarea_ejemplo:
            return jsonify({
                'mensaje': 'Tarea obtenida exitosamente',
                'tarea': tarea_ejemplo
            }), 200
        else:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
    @app.route("/tareas/<int:id>p", methods=['PUT'])
    def actualizar_tarea(id):
        data = request.get_json()
        if not data or 'titulo' not in data or 'descripcion' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400

        # Aquí deberías actualizar la tarea en la base de datos
        tarea_actualizada = {
            'id': id,
            'titulo': data['titulo'],
            'descripcion': data['descripcion'],
            'fecha_creacion': datetime.now().isoformat()
        }

        return jsonify({
            'mensaje': 'Tarea actualizada exitosamente',
            'tarea': tarea_actualizada
        }), 200
    
    @app.route("/tareas/<int:id>d", methods=['DELETE'])
    def eliminar_tarea(id):
        # Aquí deberías eliminar la tarea de la base de datos
        return jsonify({'mensaje': 'Tarea eliminada exitosamente'}), 200