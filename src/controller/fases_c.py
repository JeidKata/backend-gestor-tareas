from app import app
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_controller import FlaskController
from src.models.fase_m import Fase
from src.models import session

class FasesController(FlaskController):
    @app.route("/fases", methods=['POST'])
    def crear_fases():
        data = request.get_json()
        if not data or 'nombre' not in data:
            return jsonify({"error": "Se requiere el 'nombre' para crear una fase."}), 400

        nombre = data['nombre']
        try:
            nueva_fase = Fase.crear_fase(nombre=nombre) # Llama al método de clase
            return jsonify(nueva_fase.to_dict()), 201 # 201 Created
        except Exception as e:
            session.rollback() # Importante hacer rollback en caso de error
            return jsonify({"error": f"Error al crear la fase: {str(e)}"}), 500

    @app.route("/fases", methods=['GET']) # Nueva ruta para listar fases
    def listar_fases_api():
        fases = session.query(Fase).all() # Obtener todas las fases de la DB
        fases_data = [fase.to_dict() for fase in fases]
        return jsonify({"fases": fases_data})

    @app.route("/fases/<int:id>", methods=['GET'])
    def obtener_fase(id):
        fase = Fase.obtener_fase_por_id(id)
        if fase:
            return jsonify(fase)
        else:
            return jsonify({"error": "Fase no encontrada"}), 404
        
    @app.route("/fases/<int:id>p", methods=['PUT'])
    def actualizar_fase(id):
        data = request.get_json()
        if not data or 'nombre' not in data:
            return jsonify({"error": "Se requiere el 'nombre' para actualizar la fase."}), 400

        nombre = data['nombre']
        fase = Fase.obtener_fase_por_id(id)
        if not fase:
            return jsonify({"error": "Fase no encontrada"}), 404

        try:
            fase_actualizada = Fase.actualizar_fase(id, nombre)
            if fase_actualizada:
                return jsonify(fase_actualizada), 200
            else:
                return jsonify({"error": "No se pudo actualizar la fase"}), 500
        except Exception as e:
            session.rollback()
            return jsonify({"error": f"Error al actualizar la fase: {str(e)}"}), 500
        
    @app.route("/fases/<int:id>d", methods=['DELETE'])
    def eliminar_fase(id):
        fase = Fase.obtener_fase_por_id(id)
        if not fase:
            return jsonify({"error": "Fase no encontrada"}), 404

        try:
            if Fase.eliminar_fase(id):
                return jsonify({"message": "Fase eliminada exitosamente"}), 200
            else:
                return jsonify({"error": "No se pudo eliminar la fase"}), 500
        except Exception as e:
            session.rollback()
            return jsonify({"error": f"Error al eliminar la fase: {str(e)}"}), 500
        