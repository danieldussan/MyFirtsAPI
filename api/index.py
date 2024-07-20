import os
from flask import Flask, jsonify, request
import pymysql
from flask_cors import CORS
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = "mysecretkey"

# Configuración directamente en el archivo
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as ex:
        app.logger.error(f"Error in get_db_connection: {ex}")
        raise

@app.route('/getusers', methods=['GET'])
def get_all():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = 'SELECT * FROM users'
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = [{'documento': fila['documento'], 'nombre': fila['nombre'], 'apellido': fila['apellido'], 'carrera': fila['carrera']} for fila in datos]
        connection.close()
        return jsonify({'usuarios': usuarios, 'mensaje': "Usuarios listados"})
    except Exception as ex:
        return jsonify({'mensaje': f"Error al listar usuarios, error: {ex}"}), 500

@app.route('/usuario/<documento>', methods=['GET'])
def leer_usuario(documento):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "SELECT * FROM users WHERE documento = %s"
        cursor.execute(sql, (documento,))
        datos = cursor.fetchone()
        connection.close()
        if datos:
            usuario = {'documento': datos['documento'], 'nombre': datos['nombre'] + ' ' + datos['apellido'], 'carrera': datos['carrera']}
            return jsonify({'usuario': usuario, 'mensaje': "Usuario encontrado por documento"}), 200
        else:
            return jsonify({'mensaje': "Usuario no encontrado"}), 400
    except Exception as ex:
        return jsonify({'mensaje': f"Error al listar usuarios por documento, error: {ex}"}), 500

@app.route('/usuario', methods=['POST'])
def registrar_usuario():
    try:
        consulta = request.json
        documento = consulta.get('documento')
        if verificar_usuario_existe(documento):
            return jsonify({'mensaje': f"El documento '{documento}' ya existe en la base de datos."}), 400
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "INSERT INTO users (documento, nombre, apellido, carrera) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (consulta['documento'], consulta['nombre'], consulta['apellido'], consulta['carrera']))
        connection.commit()
        connection.close()
        return jsonify({'mensaje': "Usuario registrado"}), 200
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {ex}"}), 500

@app.route('/usuario/<documento>', methods=['PUT'])
def actualizar_usuario(documento):
    try:
        consulta = request.json
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "UPDATE users SET nombre = %s, apellido = %s, carrera = %s WHERE documento = %s"
        cursor.execute(sql, (consulta['nombre'], consulta['apellido'], consulta['carrera'], documento))
        connection.commit()
        connection.close()
        return jsonify({'mensaje': "Usuario actualizado"}), 200
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {ex}"}), 500

@app.route('/usuario/<documento>', methods=['DELETE'])
def eliminar_usuario(documento):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "DELETE FROM users WHERE documento = %s"
        cursor.execute(sql, (documento,))
        connection.commit()
        connection.close()
        return jsonify({'mensaje': f"El usuario con el documento: {documento} ha sido eliminado"}), 200
    except Exception as ex:
        return jsonify({'mensaje': f"Error al eliminar registro: {ex}"}), 500

def verificar_usuario_existe(documento):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql_consulta = "SELECT documento FROM users WHERE documento = %s"
        cursor.execute(sql_consulta, (documento,))
        resultado = cursor.fetchone()
        connection.close()
        return bool(resultado)
    except Exception as ex:
        print(f"Error en la consulta SQL: {ex}")
        return None

@app.route('/sendDato', methods=['POST'])
def send_dato():
    try:
        return jsonify({"mensaje": "Exitoso"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)}), 500

def page_not_found(error):
    return "<h1>Pagina no encontrada</h1>", 404

if __name__ == '__main__':
    app.register_error_handler(404, page_not_found)
    app.run(host='0.0.0.0')
