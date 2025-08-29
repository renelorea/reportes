from flask import Blueprint, redirect, url_for, session
from app.controllers import auth_controller

# Creamos un Blueprint para agrupar las rutas de autenticación
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    if 'loggedin' in session:
        return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.login_page'))

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return auth_controller.show_login_form()

@auth_bp.route('/login', methods=['POST'])
def login_submit():
    return auth_controller.login()

@auth_bp.route('/dashboard')
def dashboard():
    return auth_controller.dashboard()

@auth_bp.route('/logout')
def logout():
    return auth_controller.logout()