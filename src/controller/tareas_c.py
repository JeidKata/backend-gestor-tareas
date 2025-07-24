from app import app
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_controller import FlaskController
from datetime import datetime

@app.route('/')
def home():
    return "<h1>¡Aplicación Flask corriendo correctamente!</h1>"

