import click
from flask.cli import with_appcontext
from app.models.user_model import User

@click.command(name='add-user')
@with_appcontext
def add_user_command():
    email = "test@escuela.edu"
    password = "password123"
    
    if User.find_by_email(email):
        print(f"El usuario '{email}' ya existe.")
        return

    if User.create('Usuario', 'Prueba', email, 'Profesor', password):
        print(f"Usuario '{email}' con contraseña '{password}' añadido exitosamente.")
    else:
        print(f"No se pudo crear el usuario '{email}'.")