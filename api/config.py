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
    MYSQL_PORT = int(os.getenv('MYSQL_PORT'))

config = {
    'Development': DevelopmentConfig
}
