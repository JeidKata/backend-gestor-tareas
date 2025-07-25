#!/usr/bin/env python3
"""
Script para generar automáticamente controladores Flask-RESTX 
a partir de los controladores Flask existentes.
"""

import os
import re
from pathlib import Path

# Configuración del generador
CONTROLLERS_DIR = "src/controller"
MODELS_DIR = "src/models"
OUTPUT_SUFFIX = "_restx.py"

# Plantilla base para controladores Flask-RESTX
RESTX_TEMPLATE = '''from flask_restx import Namespace, Resource, fields
from flask import request
from src.models.{model_file} import {model_class}
from src.models import session

# Namespace para {entity}
{namespace_var} = Namespace(
    '{entity_lower}', 
    description='Operaciones CRUD para {entity_plural}'
)

# Modelos para Swagger
{entity_lower}_model = {namespace_var}.model('{model_class}', {{
{model_fields}
}})

{entity_lower}_input = {namespace_var}.model('{model_class}Input', {{
{input_fields}
}})

{entity_lower}_response = {namespace_var}.model('{model_class}Response', {{
    'mensaje': fields.String(description='Mensaje de respuesta'),
    '{entity_lower}': fields.Nested({entity_lower}_model)
}})

@{namespace_var}.route('/')
class {model_class}List(Resource):
    @{namespace_var}.doc('listar_{entity_lower}s')
    @{namespace_var}.marshal_list_with({entity_lower}_model)
    def get(self):
        """Obtener todas las {entity_lower}s"""
        try:
            {entity_lower}s = {model_class}.obtener_{entity_lower}s()
            return {entity_lower}s, 200
        except Exception as e:
            {namespace_var}.abort(500, f"Error interno: {{str(e)}}")

    @{namespace_var}.doc('crear_{entity_lower}')
    @{namespace_var}.expect({entity_lower}_input)
    @{namespace_var}.marshal_with({entity_lower}_response, code=201)
    def post(self):
        """Crear una nueva {entity_lower}"""
        try:
            data = request.get_json()
            {entity_lower}_nuevo = {model_class}.crear_{entity_lower}(**data)
            return {{
                'mensaje': '{entity_class} creada exitosamente',
                '{entity_lower}': {entity_lower}_nuevo
            }}, 201
        except Exception as e:
            session.rollback()
            {namespace_var}.abort(500, f"Error al crear {entity_lower}: {{str(e)}}")

@{namespace_var}.route('/<int:id>')
@{namespace_var}.param('id', 'ID de la {entity_lower}')
class {model_class}Resource(Resource):
    @{namespace_var}.doc('obtener_{entity_lower}')
    @{namespace_var}.marshal_with({entity_lower}_model)
    def get(self, id):
        """Obtener una {entity_lower} específica"""
        try:
            {entity_lower} = {model_class}.obtener_{entity_lower}_por_id(id)
            if {entity_lower}:
                return {entity_lower}, 200
            else:
                {namespace_var}.abort(404, "{entity_class} no encontrada")
        except Exception as e:
            {namespace_var}.abort(500, f"Error interno: {{str(e)}}")

    @{namespace_var}.doc('actualizar_{entity_lower}')
    @{namespace_var}.expect({entity_lower}_input)
    @{namespace_var}.marshal_with({entity_lower}_response)
    def put(self, id):
        """Actualizar una {entity_lower}"""
        try:
            data = request.get_json()
            {entity_lower}_actualizada = {model_class}.actualizar_{entity_lower}(id, **data)
            if {entity_lower}_actualizada:
                return {{
                    'mensaje': '{entity_class} actualizada exitosamente',
                    '{entity_lower}': {entity_lower}_actualizada
                }}, 200
            else:
                {namespace_var}.abort(404, "{entity_class} no encontrada")
        except Exception as e:
            session.rollback()
            {namespace_var}.abort(500, f"Error al actualizar {entity_lower}: {{str(e)}}")

    @{namespace_var}.doc('eliminar_{entity_lower}')
    def delete(self, id):
        """Eliminar una {entity_lower}"""
        try:
            if {model_class}.eliminar_{entity_lower}(id):
                return {{'mensaje': '{entity_class} eliminada exitosamente'}}, 200
            else:
                {namespace_var}.abort(404, "{entity_class} no encontrada")
        except Exception as e:
            session.rollback()
            {namespace_var}.abort(500, f"Error al eliminar {entity_lower}: {{str(e)}}")
'''

def extract_model_info(model_file_path):
    """Extrae información del modelo desde el archivo Python"""
    with open(model_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar la clase del modelo
    class_match = re.search(r'class (\w+)\(Base\):', content)
    if not class_match:
        return None
    
    model_class = class_match.group(1)
    
    # Buscar campos de SQLAlchemy
    fields = []
    field_patterns = re.findall(r'(\w+)\s*=\s*Column\((.*?)\)', content, re.MULTILINE)
    
    for field_name, field_def in field_patterns:
        if field_name in ['id']:
            continue
            
        # Determinar tipo de campo para Swagger
        field_type = 'fields.String()'
        if 'Integer' in field_def:
            field_type = 'fields.Integer()'
        elif 'DateTime' in field_def:
            field_type = 'fields.DateTime()'
        elif 'Text' in field_def:
            field_type = 'fields.String()'
        elif 'Boolean' in field_def:
            field_type = 'fields.Boolean()'
        
        # Determinar si es requerido
        required = 'nullable=False' in field_def and 'default=' not in field_def
        if required:
            field_type = field_type.replace('()', f'(required=True, description="{field_name.replace("_", " ").title()}")')
        else:
            field_type = field_type.replace('()', f'(description="{field_name.replace("_", " ").title()}")')
        
        fields.append(f"    '{field_name}': {field_type}")
    
    return {
        'model_class': model_class,
        'fields': fields
    }

def generate_restx_controller(entity_name, model_info):
    """Genera un controlador Flask-RESTX basado en la información del modelo"""
    
    model_fields = ',\n'.join(model_info['fields'] + [
        "    'id': fields.Integer(description='ID único')"
    ])
    
    # Campos de entrada (sin ID para creación)
    input_fields = ',\n'.join(model_info['fields'])
    
    # Variables para la plantilla
    template_vars = {
        'model_file': f"{entity_name.lower()}_m",
        'model_class': model_info['model_class'],
        'entity': entity_name.title(),
        'entity_class': entity_name.title(),
        'entity_lower': entity_name.lower(),
        'entity_plural': f"{entity_name.lower()}s",
        'namespace_var': f"{entity_name.lower()}_ns",
        'model_fields': model_fields,
        'input_fields': input_fields
    }
    
    return RESTX_TEMPLATE.format(**template_vars)

def main():
    """Función principal del generador"""
    print("🤖 Generador automático de controladores Flask-RESTX")
    print("=" * 50)
    
    # Entidades a procesar
    entities = ['tablero', 'fase', 'persona']
    
    for entity in entities:
        print(f"\n📝 Procesando: {entity}")
        
        # Ruta del modelo
        model_file = f"{MODELS_DIR}/{entity}_m.py"
        if not os.path.exists(model_file):
            print(f"  ❌ Modelo no encontrado: {model_file}")
            continue
        
        # Extraer información del modelo
        model_info = extract_model_info(model_file)
        if not model_info:
            print(f"  ❌ No se pudo analizar el modelo: {model_file}")
            continue
        
        # Generar controlador
        restx_code = generate_restx_controller(entity, model_info)
        
        # Guardar archivo
        output_file = f"{CONTROLLERS_DIR}/{entity}_restx.py"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(restx_code)
        
        print(f"  ✅ Generado: {output_file}")
    
    print(f"\n🎉 ¡Generación completada!")
    print(f"\n📋 Archivos generados:")
    for entity in entities:
        print(f"  - {CONTROLLERS_DIR}/{entity}_restx.py")
    
    print(f"\n🔧 Próximos pasos:")
    print(f"  1. Revisar y ajustar los archivos generados")
    print(f"  2. Registrar los namespaces en app_con_swagger.py")
    print(f"  3. Probar la documentación en /docs/")

if __name__ == "__main__":
    main()
