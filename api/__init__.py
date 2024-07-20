# api/__init__.py

from flask import Flask
from flask_cors import CORS
from .config import DevelopmentConfig

app = Flask(__name__)
CORS(app)
app.secret_key = "mysecretkey"

# Cargar configuración
app.config.from_object(DevelopmentConfig)

# Ahora puedes importar tus rutas u otros componentes
from . import index  # Asegúrate de que las rutas están en index.py
