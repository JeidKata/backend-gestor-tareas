from app import app
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_controller import FlaskController
from datetime import datetime

class TableroController(FlaskController):
    @app.route("/tablero", methods=['POST'])
    def manejar_tablero():
        data = request.get_json()
        if not data or 'id' not in data or 'descripcion' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400

        tarea = {
            'id': data['id'],
            'nombre': data['nombre'],
            'descripcion': data['descripcion'],
            'fecha_creacion': datetime.now().isoformat(),
            'fecha_entrega': data.get('fecha_entrega', None),
            'estado': data['estado', 'pendiente']
        }

        # Aquí deberías guardar la tarea en la base de datos
        # Por ahora, solo devolvemos la tarea creada como ejemplo

        return jsonify({'mensaje': 'Tarea creada exitosamente', 'tarea': tarea}), 201
    
    @app.route("/tablero", methods=['GET'])
    def obtener_tableros():
        # Aquí deberías obtener la lista de tablero de la base de datos
        # Por ahora, devolvemos una lista de ejemplo
        tablero_ejemplo = [
            {
                'id': 1,
                'nombre': 'Tarea de ejemplo 1',
                'descripcion': 'Esta es una tarea de ejemplo',
                'fecha_creacion': datetime.now().isoformat(),
                'fecha_entrega': '30/07/2025',
                'estado': 'pendiente'
            },
            {
                'id': 2,
                'nombre': 'Tarea de ejemplo 2',
                'descripcion': 'Otra tarea de ejemplo',
                'fecha_creacion': datetime.now().isoformat(),
                'fecha_entrega': '30/08/2025',
                'estado': 'completada'
            }
        ]
        return jsonify({'tablero': tablero_ejemplo}), 200
    
    @app.route("/tablero/<int:id>g", methods=['GET'])
    def obtener_tablero(id):
        # Aquí deberías buscar la tablero por ID en la base de datos
        # Por ahora devolvemos una tablero de ejemplo
        tablero_ejemplo = {
            'id': id,
            'nombre': f'tablero de ejemplo {id}',
            'descripcion': f'Descripción de la tablero {id}',
            'fecha_creacion': datetime.now().isoformat(),
            'fecha_entrega': '30/07/2025',
            'estado': 'pendiente'
        }
        return jsonify({'tablero': tablero_ejemplo}), 200
    
    @app.route("/tablero/<int:id>p", methods=['PUT'])
    def actualizar_tablero(id):
        data = request.get_json()
        if not data or 'nombre' not in data or 'descripcion' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400

        tablero_actualizada = {
            'id': id,
            'nombre': data['nombre'],
            'descripcion': data['descripcion'],
            'fecha_creacion': datetime.now().isoformat(),
            'fecha_entrega': data.get('fecha_entrega', None),
            'estado': data.get('estado', 'pendiente')
        }

        return jsonify({'mensaje': 'tablero actualizada exitosamente', 'tablero': tablero_actualizada}), 200
    
    @app.route("/tablero/<int:id>d", methods=['DELETE'])
    def eliminar_tablero(id):
        # Aquí deberías eliminar la tablero de la base de datos
        # Por ahora, devolvemos un mensaje de éxito como ejemplo
        return jsonify({'mensaje': 'Tarea eliminada exitosamente'}), 200
