from app import app
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_controller import FlaskController

class PersonaController(FlaskController):
    @app.route("/personas", methods = ['POST'])
    def crear_persona():
        data = request.get_json()
        if not data or 'nombre' not in data or 'edad' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400

        persona = {
            'nombre': data['nombre'],
            'edad': data['edad']
        }

        # Aquí deberías guardar la persona en la base de datos
        # Por ahora, solo devolvemos la persona creada como ejemplo

        return jsonify({'mensaje': 'Persona creada exitosamente', 'persona': persona}), 201
    
    @app.route("/personas", methods = ['GET'])
    def obtener_personas():
        # Aquí deberías obtener la lista de personas de la base de datos
        # Por ahora, devolvemos una lista de ejemplo
        personas_ejemplo = [
            {'id': 1, 'nombre': 'Juan', 'correo': "juan@example.com", 'password': "1234"},
            {'id': 2, 'nombre': 'Marta', 'correo': "marta@example.com", 'password': "5678"}
        ]
        return jsonify({'personas': personas_ejemplo}), 200
    
    @app.route("/personas/<int:id>g", methods = ['GET'])
    def obtener_persona(id):
        # Aquí deberías buscar la persona por ID en la base de datos
        # Por ahora devolvemos una persona de ejemplo
        persona_ejemplo = {
            'id': id,
            'nombre': f'{id.nombre}',
            'correo': f'{id.correo}',
            'password': f'{id.password}'
        }        
        return jsonify({'persona': persona_ejemplo}), 200
    
    @app.route("/personas/<int:id>p", methods = ['PUT'])
    def actualizar_persona(id):
        data = request.get_json()
        if not data or 'nombre' not in data or 'edad' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400

        # Aquí deberías actualizar la persona en la base de datos
        # Por ahora, devolvemos la persona actualizada como ejemplo
        persona_actualizada = {
            'id': id,
            'nombre': data['nombre'],
            'edad': data['edad']
        }

        return jsonify({'mensaje': 'Persona actualizada exitosamente', 'persona': persona_actualizada}), 200
    
    @app.route("/personas/<int:id>d", methods = ['DELETE'])
    def eliminar_persona(id):
        # Aquí deberías eliminar la persona de la base de datos
        return jsonify({'mensaje': 'Persona eliminada exitosamente'}), 200