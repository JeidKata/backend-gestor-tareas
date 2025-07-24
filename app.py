from flask import Flask
from models import Base, engine
from flask_controller import FlaskControllerRegister
from flask_cors import CORS

app = Flask(__name__)

@app.route('/')
def home():
    return "¡Aplicación Flask corriendo correctamente!"

#se agrega el cors a la app y se configura para que solo acepte peticiones con el header Content-Type
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#se crea la llave para la sesion
app.secret_key = 'llave_para_sesion'
app.debug = True

register = FlaskControllerRegister(app)
register.register_package("src.controller")

Base.metadata.create_all(engine)

if __name__ == '__main__':
    app.run(debug=True)