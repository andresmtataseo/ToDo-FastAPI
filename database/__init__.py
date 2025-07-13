from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import config

def create_database_if_not_exists():
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    try:
        host = config['DB_HOST']
        port = config['DB_PORT']

        conn = psycopg2.connect(
            dbname='postgres',
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
            host=host, 
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Verificar si la base de datos ya existe
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{config['DB_NAME']}'")
        exists = cursor.fetchone()

        if not exists:
            # Crear la base de datos si no existe
            print(f"Creando base de datos: {config['DB_NAME']}")
            cursor.execute(f"CREATE DATABASE {config['DB_NAME']}")
            print(f"Base de datos {config['DB_NAME']} creada exitosamente.")
        else:
            print(f"La base de datos {config['DB_NAME']} ya existe.")

        # Cerrar la conexion
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al conectar o crear la base de datos: {e}")

# Ejecutar la funcion para crear la base de datos si no existe
create_database_if_not_exists()

# String que conecta SQLAlchemy con PostgreSQL
DATABASE_URL = f'postgresql+psycopg2://{config["DB_USER"]}:{config["DB_PASSWORD"]}@{config["DB_HOST"]}:{config["DB_PORT"]}/{config["DB_NAME"]}'

# Crear motor de conexion de PostgreSQL
engine = create_engine(DATABASE_URL)

# Crear tienda de sesiones de conexion con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para todos nuestros modelos (tablas) de base de datos 
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
