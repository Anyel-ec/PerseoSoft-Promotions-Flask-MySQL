from flask import Flask, render_template, request
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
        # Obtener el código de barras y el código de promoción del formulario
        codigo_barras = request.args.get('codigo_barras')
        codigo_promocion = request.args.get('codigo_promocion')

        # Crear una conexión y un cursor
        cur = mysql.connection.cursor()

        # Consulta SQL para buscar productos por código de barras o código de promoción
        query = """
            SELECT P.ProductoID, P.Nombre AS NombreProducto, P.Descripcion AS DescripcionProducto, P.Precio
            FROM Productos AS P
            JOIN Productos_Promocion AS PP ON P.ProductoID = PP.ProductoID
            JOIN DosxUno AS D ON PP.PromocionID = D.PromocionID
            WHERE P.CodigoBarras = %s OR D.codigoPromocion = %s
        """

        # Ejecutar la consulta
        cur.execute(query, (codigo_barras, codigo_promocion))

        # Obtener resultados
        data = cur.fetchall()

        # Imprimir resultados en la consola
        print("Resultados de búsqueda de producto:", data)

        # Cerrar la conexión
        cur.close()

        # Renderizar la plantilla con los resultados
        return render_template('index.html', data=data, mensaje="Búsqueda exitosa.")
    except Exception as e:
        # Si hay un error, renderizar la plantilla con un mensaje de error
        return render_template('index.html', mensaje=f"Error en la búsqueda del producto: {str(e)}")

    try:
        # Obtener el código de barras del formulario
        codigo_barras = request.args.get('codigo_barras')

        # Crear una conexión y un cursor
        cur = mysql.connection.cursor()

        # Ejecutar una consulta para buscar el producto por código de barras
        cur.execute("SELECT * FROM Productos WHERE CodigoBarras = %s", (codigo_barras,))

        # Obtener resultados
        data = cur.fetchall()

        # Imprimir resultados en la consola
        print("Resultados de búsqueda de producto:", data)

        # Cerrar la conexión
        cur.close()

        # Renderizar la plantilla con los resultados
        return render_template('index.html', data=data, mensaje="Búsqueda exitosa.")
    except Exception as e:
        # Si hay un error, renderizar la plantilla con un mensaje de error
        return render_template('index.html', mensaje=f"Error en la búsqueda del producto: {str(e)}")

@app.route('/buscar_promocion', methods=['GET'])
def buscar_promocion():
    try:
        # Obtener el código de promoción del formulario
        codigo_promocion = request.args.get('codigo_promocion')

        # Crear una conexión y un cursor
        cur = mysql.connection.cursor()

        # Ejecutar una consulta para buscar la promoción por código
        cur.execute("SELECT * FROM DosxUno WHERE codigoPromocion = %s", (codigo_promocion,))

        # Obtener resultados
        promocion = cur.fetchone()

        if not promocion:
            # Imprimir resultados en la consola
            print("Promoción no encontrada.")

            return render_template('index.html', mensaje="Promoción no encontrada.")

        # Imprimir resultados en la consola
        print("Resultados de búsqueda de promoción:", promocion)

        # Ejecutar una consulta para obtener los productos asociados a la promoción
        cur.execute("""
           SELECT
                    P.ProductoID,
                    P.Nombre AS NombreProducto,
                    P.Descripcion AS DescripcionProducto,
                    P.Precio,
                FROM Productos AS P
            JOIN Productos_Promocion AS PP ON P.ProductoID = PP.ProductoID
            WHERE PP.PromocionID = %s
        """, (promocion['PromocionID'],))

        # Obtener resultados
        productos_promocion = cur.fetchall()

        # Cerrar la conexión
        cur.close()

        # Renderizar la plantilla con los resultados
        return render_template('index.html', promocion=promocion, data=productos_promocion, mensaje="Búsqueda de promoción exitosa.")


    except Exception as e:
        # Si hay un error, renderizar la plantilla con un mensaje de error
        return render_template('index.html', mensaje=f"Error en la búsqueda de la promoción: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
