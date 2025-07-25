from app import app
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_controller import FlaskController
from datetime import datetime
from src.models.tarea_m import Tarea
from src.models import session

@app.route('/')
def home():
    # "<h1>¡Aplicación Flask corriendo correctamente!</h1>"
    return {
        'mensaje': '¡API Gestor de Tareas funcionando!',
        'documentacion': '/docs/',
        'version': '1.0'
    }

class ClientesController(FlaskController):
    @app.route("/tareas", methods=['GET', 'POST'])
    def manejar_tareas():
        if request.method == 'POST':
            # Crear tarea
            data = request.get_json()
            if not data or 'nombre' not in data or 'descripcion' not in data:
                return jsonify({'error': 'Datos incompletos'}), 400

            nombre= data['nombre']
            descripcion= data['descripcion']
            # fecha_inicio = data['fecha_inicio']
            fecha_inicio_str = data.get('fecha_inicio')
            # fecha_fin = data['fecha_fin']
            fecha_fin_str = data.get('fecha_fin')
            fase_id= data['fase_id']
            persona_id= data['persona_id']
            tablero_id= data['tablero_id']

            # Convertir fechas de string a datetime
            # Asegurar que el formato sea YYYY-MM-DD
            fecha_inicio = None # Inicializa como None
            fecha_fin = None # Inicializa como None
            if fecha_inicio_str and fecha_fin_str:
                try:
                    # Aquí es donde se convierte el string a un objeto datetime
                    fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
                    fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d')
                except ValueError:
                    return jsonify({"error": "Formato de fecha_entrega inválido. Use YYYY-MM-DD."}), 400
                
                try:
                    tarea_nueva = Tarea.crear_tarea(nombre=nombre, descripcion=descripcion,
                                            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin,
                                            fase_id=fase_id, persona_id=persona_id, tablero_id=tablero_id)
                    return jsonify({'mensaje': 'Tarea creada exitosamente', 'tarea': tarea_nueva}), 201
                except Exception as e:
                    session.rollback()
                    return jsonify({"error": f"Error al crear la tarea: {str(e)}"}), 500
            
        elif request.method == 'GET':
            tareas = Tarea.listar_tareas()
            return jsonify({ 
                'mensaje': 'Tareas obtenidas exitosamente',
                'tareas': tareas, 'total': len(tareas)
            }), 200

    @app.route("/tareas/<int:id>g", methods=['GET'])
    def obtener_tarea(id):
        tarea = Tarea.obtener_tarea_por_id(id)
        if tarea:
            return jsonify({
                'mensaje': 'Tarea obtenida exitosamente',
                'tarea': tarea
            }), 200
        else:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
    @app.route("/tareas/<int:id>p", methods=['PUT'])
    def actualizar_tarea(id):
        data = request.get_json()
        if not data or 'nombre' not in data or 'descripcion' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400

        nombre= data['nombre']
        descripcion= data['descripcion']
        fecha_inicio_str = data.get('fecha_inicio')
        fecha_fin_str = data.get('fecha_fin')
        fase_id= data['fase_id']
        persona_id= data['persona_id']
        tablero_id= data['tablero_id']

        fecha_inicio = None # Inicializa como None
        fecha_fin = None # Inicializa como None
        if fecha_inicio_str and fecha_fin_str:
            try:
                # Aquí es donde se convierte el string a un objeto datetime
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d')
            except ValueError:
                return jsonify({"error": "Formato de fecha_entrega inválido. Use YYYY-MM-DD."}), 400

        try:
            tarea_actualizada = Tarea.actualizar_tarea(id, nombre=nombre, descripcion=descripcion,
                                                        fecha_inicio=fecha_inicio, fecha_fin=fecha_fin,
                                                        fase_id=fase_id, persona_id=persona_id, tablero_id=tablero_id)
            if tarea_actualizada:
                return jsonify({
                    'mensaje': 'Tarea actualizada exitosamente',
                    'tarea': tarea_actualizada
                }), 200  
            else: 
                return jsonify({
                    'mensaje': 'Tarea no encontrada',
                }), 404
        except Exception as e:
            session.rollback()
            return jsonify({"error": f"Error interno al actualizar la tarea: {str(e)}"}), 500
            

    @app.route("/tareas/<int:id>d", methods=['DELETE'])
    def eliminar_tarea(id):
        if Tarea.eliminar_tarea(id):
            return jsonify({'mensaje': 'Tarea eliminada exitosamente'}), 200
        return jsonify({'mensaje': 'Tarea no encontrada'}), 404