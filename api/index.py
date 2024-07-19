from flask import Flask, jsonify, request
import pymysql
from flask_cors import CORS
from config import Config

app = Flask(__name__)
CORS(app)

def get_db_connection():
    connection = pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

app.secret_key = "mysecretkey"

#############################################################
# PARA CONSULTAR TODOS DATOS DE LA BASE DE DATOS DE UNA TABLA #
#############################################################
@app.route('/usuario', methods=['GET'])
def get_all():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = 'SELECT * FROM usuarios'
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = []
        for fila in datos:
            usuario = {'documento': fila['documento'], 'nombre': fila['nombre'], 'apellido': fila['apellido'], 'carrera': fila['carrera']}
            usuarios.append(usuario)
        connection.close()
        return jsonify({'usuarios': usuarios, 'mensaje': "Usuarios listados"})
    except Exception as ex:
        return jsonify({'mensaje': "Error al listar usuarios"}), 500

##########################################################
# PARA CONSULTAR DATOS A LA BASE DE DATOS CON UN PARAMETRO #
##########################################################
@app.route('/usuario/<documento>', methods=['GET'])
def leer_usuario(documento):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "SELECT * FROM usuarios WHERE documento = %s"
        valores = (documento,)
        cursor.execute(sql, valores)
        datos = cursor.fetchone()
        connection.close()
        if datos:
            usuario = {'documento': datos['documento'], 'nombre': datos['nombre'] + ' ' + datos['apellido'], 'carrera': datos['carrera']}
            return jsonify({'usuario': usuario, 'mensaje': "Usuario encontrado por documento"}), 200
        else:
            return jsonify({'mensaje': "Usuario no encontrado"}), 400
    except Exception as ex:
        return jsonify({'mensaje': f"Error al listar usuarios por documento, error: {ex}"}), 500

#########################################
# PARA INSERTAR DATOS A LA BASE DE DATOS #
#########################################
@app.route('/usuario', methods=['POST'])
def registrar_usuario():
    try:
        consulta = request.json
        documento = consulta.get('documento')
        resultado = verificar_usuario_existe(documento)
        if resultado:
            return jsonify({'mensaje': f"El documento '{documento}' ya existe en la base de datos."}), 400
        else:
            connection = get_db_connection()
            cursor = connection.cursor()
            sql = """INSERT INTO usuarios (documento, nombre, apellido, carrera) 
                     VALUES (%s, %s, %s, %s)"""
            valores = (consulta['documento'], consulta['nombre'], consulta['apellido'], consulta['carrera'])
            cursor.execute(sql, valores)
            connection.commit()
            connection.close()
            return jsonify({'mensaje': "Usuario registrado"}), 200
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {ex}"}), 500

#############################################################
# PARA ACTUALIZAR UN REGISTRO DE UNA TABLA DE LA BD #
#############################################################
@app.route('/usuario/<documento>', methods=['PUT'])
def actualizar_usuario(documento):
    try:
        consulta = request.json
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = """UPDATE usuarios SET nombre = %s, apellido = %s, carrera = %s WHERE documento = %s"""
        valores = (consulta['nombre'], consulta['apellido'], consulta['carrera'], documento)
        cursor.execute(sql, valores)
        connection.commit()
        connection.close()
        return jsonify({'mensaje': "Usuario actualizado"}), 200
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {ex}"}), 500

#############################################################
# PARA ELIMINAR UN REGISTRO DE UNA TABLA DE LA BD #
#############################################################
@app.route('/usuario/<documento>', methods=['DELETE'])
def eliminar_usuario(documento):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "DELETE FROM usuarios WHERE documento = %s"
        cursor.execute(sql, (documento,))
        connection.commit()
        connection.close()
        return jsonify({'mensaje': f"El usuario con el documento: {documento} ha sido eliminado"}), 200
    except Exception as ex:
        return jsonify({'mensaje': f"Error al eliminar registro: {ex}"}), 500

##########################################################
# FUNCION PARA SABER SI EL USUARIO ESTA EN LA BD #
##########################################################
def verificar_usuario_existe(documento):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql_consulta = "SELECT documento FROM usuarios WHERE documento = %s"
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

##########################################################
# PAGINA DE ERROR POR DEFECTO #
##########################################################
def page_not_found(error):
    return "<h1>Pagina no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(Config)
    app.register_error_handler(404, page_not_found)
    app.run(host='0.0.0.0')
