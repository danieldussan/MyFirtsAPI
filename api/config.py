class DevelopmentConfig():
    DEBUG = True
    
    # Mysql Connection 
    MYSQL_HOST = 'localhost' 
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'esp'

Config = {
    'Development' :  DevelopmentConfig
}