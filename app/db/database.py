# Archivo: app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno (desde un archivo .env en la raíz del proyecto)
load_dotenv()

# Asegúrate de crear un archivo .env en la raíz con esto:
# DB_USER=tu_usuario_mysql
# DB_PASSWORD=tu_contraseña_mysql
# DB_HOST=localhost
# DB_NAME=diabetes_expert_system

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

# String de conexión para SQLAlchemy
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear una fábrica de sesiones para interactuar con la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que heredarán nuestros modelos
Base = declarative_base()

# Dependencia para usar en FastAPI y cerrar la conexión al terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()