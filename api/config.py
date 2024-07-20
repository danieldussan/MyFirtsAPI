import os
import dotenv

dotenv.load_dotenv()

class DevelopmentConfig:
    DEBUG = True
    
    # MySQL Connection 
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB') 

    # Depuración para asegurar que las variables de entorno se están cargando
    print(f"MYSQL_HOST: {MYSQL_HOST}")
    print(f"MYSQL_USER: {MYSQL_USER}")
    print(f"MYSQL_PASSWORD: {MYSQL_PASSWORD}")
    print(f"MYSQL_DB: {MYSQL_DB}")

config = {
    'Development': DevelopmentConfig
}
