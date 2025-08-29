from app import mysql, bcrypt

class User:
    @staticmethod
    def find_by_email(email):
        try:
            cur = mysql.connection.cursor(dictionary=True)
            cur.execute("SELECT * FROM usuarios WHERE email = %s AND activo = TRUE", (email,))
            user = cur.fetchone()
            cur.close()
            return user
        except Exception as e:
            # En una aplicación real, aquí se registraría el error en un log.
            print(f"Error al buscar usuario por email: {e}")
            return None

    @staticmethod
    def check_password(hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)

    @staticmethod
    def create(nombres, apellido_paterno, email, rol, password):
        try:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO usuarios (nombres, apellido_paterno, email, rol, contrasena) VALUES (%s, %s, %s, %s, %s)",
                (nombres, apellido_paterno, email, rol, hashed_password)
            )
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            mysql.connection.rollback()
            return False