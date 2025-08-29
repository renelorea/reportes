from app import create_app
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5001)