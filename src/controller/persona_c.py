from app import app
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_controller import FlaskController
from src.models.persona_m import Persona
from src.models import session
from sqlalchemy.exc import IntegrityError

class PersonaController(FlaskController):
    @app.route("/personas", methods = ['POST'])
    def crear_persona():
        data = request.get_json()
        if not data or 'nombre' not in data or 'correo' not in data or 'password' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400
        nombre = data['nombre']
        correo = data['correo'] 
        password = data['password']
        try:
            nueva_persona = Persona.crear_persona(nombre=nombre, correo=correo, password=password)
            return jsonify(nueva_persona), 201
        except Exception as e:
            session.rollback()
            return jsonify({"error": f"Error al crear la persona: {str(e)}"}), 500

    @app.route("/personas", methods = ['GET'])
    def listar_personas():
        personas = Persona.obtener_personas()
        return jsonify({"personas": personas, "total": len(personas)}), 200        
    
    @app.route("/personas/<int:id>g", methods = ['GET'])
    def obtener_persona(id):
        persona = Persona.obtener_persona_por_id(id)
        if persona:
            return jsonify(persona), 200
        else:
            return jsonify({"error": "Persona no encontrada"}), 404
    
    @app.route("/personas/<int:id>p", methods = ['PUT'])
    def actualizar_persona(id):
        data = request.get_json()
        if not data or 'nombre' not in data or 'correo' not in data or 'password' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400

        nombre = data['nombre']
        correo = data['correo'] 
        password = data['password']
        # Actualizar los campos si están presentes en la solicitud
        try:
            persona_actualizada = Persona.actualizar_persona(id, nombre=nombre, correo=correo, password=password)
            if persona_actualizada:
                return jsonify({'mensaje': 'Persona actualizada exitosamente', 'persona': persona_actualizada}), 200
            else:
                return jsonify({'error': 'Persona no encontrada o no se pudo actualizar'}), 404
        except IntegrityError:
            session.rollback()
            return jsonify({"error": "El correo electrónico ya está registrado para otra persona."}), 409 # Conflicto
        except Exception as e:
            session.rollback()
            return jsonify({"error": f"Error interno al actualizar la persona: {str(e)}"}), 500

        
    @app.route("/personas/<int:id>d", methods = ['DELETE'])
    def eliminar_persona(id):
        try:
            if Persona.eliminar_persona(id):
                return jsonify({'mensaje': 'Persona eliminada exitosamente'}), 200
            else:
                return jsonify({"error": "Persona no encontrada"}), 404
        except Exception as e:
            session.rollback()
            return jsonify({"error": f"Error interno al eliminar la persona: {str(e)}"}), 500
        