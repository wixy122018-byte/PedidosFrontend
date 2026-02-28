import mysql.connector
from mysql.connector import Error


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="autonomo"
    )


def obtener_clientes():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id_client, name_client FROM Clients")
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultados


def insertar_cliente(ci, nombre, email):
    conexion = conectar()
    cursor = conexion.cursor()

    consulta = """
    INSERT INTO Clients (ci_client, name_client, email_client)
    VALUES (%s, %s, %s)
    """

    cursor.execute(consulta, (ci, nombre, email))
    conexion.commit()

    cursor.close()
    conexion.close()


def eliminar_cliente(id_cliente):
    conexion = conectar()
    cursor = conexion.cursor()

    consulta = "DELETE FROM Clients WHERE id_client = %s"
    cursor.execute(consulta, (id_cliente,))
    conexion.commit()

    filas_afectadas = cursor.rowcount

    cursor.close()
    conexion.close()

    return filas_afectadas

def actualizar_cliente(id_cliente, nuevo_email):
    # Use the conectar function defined above, not conexion.conectar()
    conexion = conectar()
    cursor = conexion.cursor()
    consulta = """
    UPDATE Clients
    SET email_client = %s
    WHERE id_client = %s
    """
    # `%s` works for any type; the driver handles conversion for integers as well
    cursor.execute(consulta, (nuevo_email, id_cliente))
    conexion.commit()
    filas = cursor.rowcount
    cursor.close()
    conexion.close()
    return filas


#CONSULTAS ESPECIFICAS#

def top3_clientes():
    conexion = conectar()
    cursor = conexion.cursor()
    consulta = """
    SELECT C.name_client, COUNT(O.id_order) AS total_pedidos
    FROM Clients C
    JOIN Orders O ON C.id_client = O.id_client
    GROUP BY C.id_client
    ORDER BY total_pedidos DESC
    LIMIT 3
    """
    cursor.execute(consulta)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos


def demanda_platos():
    conexion = conectar()
    cursor = conexion.cursor()
    consulta = """
    SELECT D.name_dish, SUM(OD.quantity) AS total_vendido
    FROM Dishes D
    JOIN Order_Details OD ON D.id_dish = OD.id_dish
    GROUP BY D.id_dish
    ORDER BY total_vendido DESC
    """
    cursor.execute(consulta)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos


def pedidos_febrero_marzo():
    conexion = conectar()
    cursor = conexion.cursor()
    consulta = """
    SELECT 
    O.id_order, C.ci_client, C.name_client, C.email_client, O.order_date, OD.quantity, D.name_dish, OD.was_dish_served
    FROM Clients as C, Orders as O, Order_Details as OD, Dishes as D
    WHERE C.id_client = O.id_client
    AND O.id_order = OD.id_order
    AND OD.id_dish = D.id_dish
    AND MONTH(O.order_date) IN (2,3)
    ORDER BY C.id_client
    """
    cursor.execute(consulta)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos


def ingresos_por_tipo_pago():
    conexion = conectar()
    cursor = conexion.cursor()
    consulta = """
    SELECT TP.name_type_payment, COUNT(O.id_order) AS total_ordenes
    FROM Type_payments TP
    JOIN Payments P ON TP.id_type_payment = P.id_type_payment
    JOIN Orders O ON P.id_payment = O.id_payment
    GROUP BY TP.id_type_payment
    ORDER BY total_ordenes DESC
    """
    cursor.execute(consulta)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos