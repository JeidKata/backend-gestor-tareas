from app import app
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_controller import FlaskController
from datetime import datetime
from src.models.tablero_m import Tablero
from src.models import session

class TableroController(FlaskController):
    @app.route("/tablero", methods=['POST'])
    def crear_tablero():
        data = request.get_json()
        if not data or 'nombre' not in data or 'descripcion' not in data or 'fecha_entrega' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400

        nombre = data['nombre']
        descripcion = data['descripcion']
        fecha_entrega = data['fecha_entrega']
        estado = data['estado']

        # Convertir fecha_entrega de string a datetime
        # Asegurar que el formato sea YYYY-MM-DD
        fecha_entrega_str = data.get('fecha_entrega') # Esto es un STRING (e.g., "2025-07-30")
        fecha_entrega = None # Inicializa como None
        if fecha_entrega_str:
            try:
                # Aquí es donde se convierte el string a un objeto datetime
                fecha_entrega = datetime.strptime(fecha_entrega_str, '%Y-%m-%d')
            except ValueError:
                return jsonify({"error": "Formato de fecha_entrega inválido. Use YYYY-MM-DD."}), 400

        
        try:
            tablero_nuevo = Tablero.crear_tablero(nombre=nombre, descripcion=descripcion, 
                                                  fecha_entrega=fecha_entrega, estado=estado)
            return jsonify(tablero_nuevo), 201
        except Exception as e:
            session.rollback()
            return jsonify({"error": f"Error al crear el tablero: {str(e)}"}), 500

    @app.route("/tablero", methods=['GET'])
    def obtener_tableros():
        tableros = Tablero.obtener_tableros()
        return jsonify({"tableros": tableros, "total": len(tableros)}), 200
    
    @app.route("/tablero/<int:id>g", methods=['GET'])
    def obtener_tablero(id):
        tablero = Tablero.obtener_tablero_por_id(id)
        if tablero:
            return jsonify(tablero), 200
        else:
            return jsonify({"error": "Tablero no encontrado"}), 404
    
    @app.route("/tablero/<int:id>p", methods=['PUT'])
    def actualizar_tablero(id):
        data = request.get_json()
        if not data or 'nombre' not in data or 'descripcion' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400
        nombre = data['nombre']
        descripcion = data['descripcion']
        fecha_entrega = data['fecha_entrega']
        estado = data['estado']

        # Convertir fecha_entrega de string a datetime
        # Asegurar que el formato sea YYYY-MM-DD
        fecha_entrega_str = data.get('fecha_entrega') # Esto es un STRING (e.g., "2025-07-30")
        fecha_entrega = None # Inicializa como None
        if fecha_entrega_str:
            try:
                # Aquí es donde se convierte el string a un objeto datetime
                fecha_entrega = datetime.strptime(fecha_entrega_str, '%Y-%m-%d')
            except ValueError:
                return jsonify({"error": "Formato de fecha_entrega inválido. Use YYYY-MM-DD."}), 400
            
        try:
            tablero_actualizado = Tablero.actualizar_tablero(id, nombre=nombre, descripcion=descripcion,
                                                            fecha_entrega=fecha_entrega, estado=estado)
            if tablero_actualizado:
                return jsonify({'mensaje': 'Tablero actualizado exitosamente', 'tablero': tablero_actualizado}), 200
            else:
                return jsonify({'error': 'Tablero no encontrado o no se pudo actualizar'}), 404
        except Exception as e:
            session.rollback()
            return jsonify({"error": f"Error interno al actualizar el tablero: {str(e)}"}), 500

    @app.route("/tablero/<int:id>d", methods=['DELETE'])
    def eliminar_tablero(id):
        if Tablero.eliminar_tablero(id):
            return jsonify({'mensaje': 'Tablero eliminado exitosamente'}), 200
        return jsonify({'error': 'Tablero no encontrado'}), 404
