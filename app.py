from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')

# Inicialización de la extensión MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    # Renderizar la plantilla de la factura
    return render_template('index.html')

@app.route('/buscar_producto', methods=['GET'])
def buscar_producto():
    try:
        # Obtener el código de barras del formulario
        codigo_barras = request.args.get('codigo_barras')

        # Crear una conexión y un cursor
        cur = mysql.connection.cursor()

        # Ejecutar una consulta para buscar el producto por código de barras
        cur.execute("SELECT * FROM Productos WHERE CodigoBarras = %s", (codigo_barras,))

        # Obtener resultados
        data = cur.fetchall()

        # Cerrar la conexión
        cur.close()

        # Renderizar la plantilla con los resultados
        return render_template('index.html', data=data, mensaje="Búsqueda exitosa.")
    except Exception as e:
        # Si hay un error, renderizar la plantilla con un mensaje de error
        return render_template('index.html', mensaje=f"Error en la búsqueda del producto: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
