from flask import Flask,jsonify,request
from flask_mysqldb import MySQL
# from flask_cors import CORS, cross_origin
from config import config

app = Flask(__name__)
conexion = MySQL(app)

# settings A partir de ese momento Flask utilizará esta clave para poder cifrar la información de la cookie
app.secret_key = "mysecretkey"

#############################################################
#PARA CONSULTAR TODOS DATOS DE LA BASE DE DATOS DE UNA TABLA#
#############################################################
@app.route('/usuario', methods =['GET'])
def getall():
    try:
        cursor = conexion.connection.cursor()
        sql = 'SELECT * FROM usuarios'
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = []
        for fila in datos:
            usuario = {'documento':fila[0],'nombre':fila[1],'apellido':fila[2], 'carrera':fila[3]}
            usuarios.append(usuario)
        return jsonify({'usuarios':usuarios, 'mensaje': "Usuarios listados"})
    except Exception as ex:
        return jsonify({'mensaje':"Error al listar usuarios"})
    

##########################################################
#PARA CONSULTAR DATOS A LA BASE DE DATOS CON UN PARAMETRO#
##########################################################
@app.route('/usuario/<documento>', methods =['GET'])
def leer_usuario(documento):
    try:
        cursor = conexion.connection.cursor()
        sql = """SELECT * FROM usuarios WHERE documento = %s """
        valores = (documento,)
        cursor.execute(sql,valores)
        datos = cursor.fetchone()
        if datos != None:
            usuario = {'documento':datos[0],'nombre':datos[1]+' '+datos[2], 'carrera':datos[3]}
            return jsonify({'usuario':usuario, 'mensaje': "Usuario encontrado por documento"}),200
        else:
            return jsonify({'usuario':usuario, 'mensaje': "Usuario no encontrado"}),400
    except Exception as ex:
        return jsonify({'mensaje':f"Error al listar usuarios por documento, erorr: {ex}"}),400


#########################################
#PARA INSERTAR DATOS A LA BASE DE DATOS #
#########################################
@app.route('/usuario', methods=['POST'])
def registrar_usuario():
    try:
        #Consulta para verificar si ya esta en la base de datos
        consulta = request.json
        print(consulta)
        # consulta = request.get_json()
        documento = consulta.get('documento')
        resultado = verificar_usuario_existe(consulta)
        if resultado:
            return jsonify({'mensaje': f"El documento '{documento}' ya existe en la base de datos."}), 400
        else:
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO usuarios (documento, nombre, apellido, carrera) 
                     VALUES('{0}', '{1}', '{2}', '{3}')""".format(
                    consulta['documento'], consulta['nombre'], consulta['apellido'], consulta['carrera'])
            cursor.execute(sql)
            conexion.connection.commit()  # Para confirmar la acción de inserción
            return jsonify({'mensaje': "Usuario registrado"}), 200
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {ex}"}), 500

#############################################################
#    PARA  ACTUALIZAR UN REGISTRO DE UNA TABLA DE LA BD     #
#############################################################

@app.route('/usuario/<documento>', methods = ['PUT'])
def actualizar_usuario(documento):
    try:
        cursor = conexion.connection.cursor()
        sql = """UPDATE usuarios SET nombre = %s, apellido = %s, carrera = %s WHERE documento = %s"""
        valores = (request.json['nombre'], request.json['apellido'], request.json['carrera'], documento)
        cursor.execute(sql, valores)
        conexion.connection.commit()  # Para confirmar la acción de inserción
        return jsonify({'mensaje': "Usuario actualizado"}), 200
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {ex}"}), 500


#############################################################
#     PARA  ELIMINAR UN REGISTRO DE UNA TABLA DE LA BD      #
#############################################################

@app.route('/usuario/<documento>', methods = ['DELETE'])
def eliminar_usuario(documento):
    try:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM usuarios WHERE documento = '{0}'".format(documento)
            cursor.execute(sql)
            conexion.connection.commit()  # Para confirmar la acción
            return jsonify({'mensaje': f"El usuario con el documento: {documento} ha sido eliminado"}), 200
    except Exception as ex:
        return jsonify({'mensaje':f"Error al eliminar registro: {ex}"}),400

##########################################################
#    FUNCION PARA SABER SI EL USUARIO ESTA EN LA BD      #
##########################################################
def verificar_usuario_existe(consulta):
    documento = consulta.get('documento')
    try:
        cursor = conexion.connection.cursor()
        sql_consulta = f"SELECT documento FROM usuarios WHERE documento = {documento}"
        cursor.execute(sql_consulta)
        resultado = cursor.fetchone()
        return bool(resultado)
    except Exception as ex:
        print(f"Error en la consulta SQL: {ex}")
        return None
    finally:
        cursor.close()

@app.route('/sendDato', methods=['POST'])
def sendDato():
    try:
        return jsonify({"mensaje":"Exitoso"})
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})
##########################################################
#               PAGINA DE ERROR POR DEFECTO              #
##########################################################
def page_not_found(error):
    return "<h1> Pagina no encontrada</h1>", 404
#Final
if __name__ == '__main__':
    app.config.from_object(config['Development'])
    app.register_error_handler(404,page_not_found)
    app.run(host='0.0.0.0')