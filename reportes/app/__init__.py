from flask import Flask
from flask_mysql_connector import MySQL
from flask_bcrypt import Bcrypt
import os

# Se inicializan las extensiones sin una aplicación específica
mysql = MySQL()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    # Carga la configuración desde el archivo config.py y las variables de entorno
    app.config.from_object('app.config.Config')
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DATABASE'] = os.getenv('MYSQL_DATABASE')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Inicializa las extensiones con la aplicación
    mysql.init_app(app)
    bcrypt.init_app(app)

    # Importar y registrar los Blueprints (grupos de rutas)
    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    
    from .routes.report_routes import report_bp
    app.register_blueprint(report_bp)


    # Importar y registrar comandos CLI
    from .commands import add_user_command
    app.cli.add_command(add_user_command)

    return app