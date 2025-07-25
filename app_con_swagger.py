from flask import Flask
from src.models import Base, engine, session
# from flask_controller import FlaskControllerRegister  # No necesario con Flask-RESTX
from flask_cors import CORS
from flask_restx import Api

app = Flask(__name__)

# Configuración de Swagger UI
api = Api(
    app, 
    doc='/docs/',  # URL para acceder a la documentación
    title='Gestor de Tareas API',
    version='1.0',
    description='API REST para gestión de tareas, proyectos y fases',
    contact='tu-email@ejemplo.com',
    authorizations={
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-API-KEY'
        }
    }
)

# Importar y registrar TODOS los namespaces
from src.controller.tareas_restx import tareas_ns
from src.controller.tablero_restx import tablero_ns
from src.controller.fase_restx import fase_ns  
from src.controller.persona_restx import persona_ns

# Registrar namespaces con rutas específicas
api.add_namespace(tareas_ns, path='/api/v1/tareas')
api.add_namespace(tablero_ns, path='/api/v1/tableros')
api.add_namespace(fase_ns, path='/api/v1/fases')
api.add_namespace(persona_ns, path='/api/v1/personas')

#se agrega el cors a la app y se configura para que solo acepte peticiones con el header Content-Type
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#se crea la llave para la sesion
app.secret_key = 'llave_para_sesion'
app.debug = True

# Mantener el registro de controladores Flask tradicionales si los necesitas
# register = FlaskControllerRegister(app)
# register.register_package("src.controller")

Base.metadata.create_all(engine)

# Ruta de inicio para verificar que la API funciona
@app.route('/')
def home():
    return {
        'mensaje': '¡API Gestor de Tareas funcionando!',
        'documentacion': '/docs/',
        'version': '1.0',
        'endpoints': {
            'tareas': '/api/v1/tareas',
            'tableros': '/api/v1/tableros', 
            'fases': '/api/v1/fases',
            'personas': '/api/v1/personas'
        }
    }

# Cierra la sesión de SQLAlchemy al final de cada petición
@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

if __name__ == '__main__':
    app.run(debug=True)
