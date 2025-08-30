from flask import render_template, request, redirect, url_for, session, flash
from app.models.user_model import User

def show_login_form():
    return render_template('login.html', title="Inicio de Sesión")

def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Email y contraseña son requeridos.', 'danger')
            return redirect(url_for('auth.login_page'))

        account = User.find_by_email(email)

        if account and User.check_password(account['contrasena'], password):
            # Creamos los datos de la sesión
            session['loggedin'] = True
            session['id'] = account['id_usuario']
            session['name'] = account['nombres']
            session['role'] = account['rol']
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Email o contraseña incorrectos.', 'danger')
            return redirect(url_for('auth.login_page'))
    
    # Si el método es GET, simplemente mostramos el formulario
    return redirect(url_for('auth.login_page'))


def dashboard():
    if 'loggedin' in session:
        return render_template('dashboard.html', name=session['name'], role=session['role'])
    return redirect(url_for('auth.login_page'))

def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('auth.login_page'))
