from app import app
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_controller import FlaskController

class FasesController(FlaskController):
    @app.route("/fases", methods=['GET'])
    def listar_fases():
        fases = [
            {"id": 1, "nombre": "Activo"},
            {"id": 2, "nombre": "Completado"},
            {"id": 3, "nombre": "En Espera"}
        ]
        return jsonify({"fases": fases})

    @app.route("/fases/<int:id>", methods=['GET'])
    def obtener_fase(id):
        fases = {
            1: {"id": 1, "nombre": "Activo"},
            2: {"id": 2, "nombre": "Completado"},
            3: {"id": 3, "nombre": "En Espera"}
        }
        fase = fases.get(id)
        if fase:
            return jsonify(fase)
        else:
            return jsonify({"error": "Fase no encontrada"}), 404
        
    @app.route("/fases/activo", methods=["GET"])
    def get_fase_activo():
        return jsonify({"fase": "activo"})

    @app.route("/fases/completado", methods=["GET"])
    def get_fase_completado():
        return jsonify({"fase": "completado"})

    @app.route("/fases/en_espera", methods=["GET"])
    def get_fase_en_espera():
        return jsonify({"fase": "en espera"})