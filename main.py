import conexion
import re
import os

def limpiar_pantalla():
    os.system("cls")

def imprimir_menu():

    limpiar_pantalla()

    print("""
    ===== SISTEMA PIZZERIA =====
    1. Mostrar clientes
    2. Insertar cliente
    3. Eliminar cliente
    4. Actualizar cliente
    5. Consultas
    6. Salir
    """)

def mostrar_clientes():
    clientes = conexion.obtener_clientes()
    print("\nLista de clientes:")
    for c in clientes:
        print(c)


def ingresar_cliente():
    ci = input("Ingrese CI: ")
    nombre = input("Ingrese nombre: ")
    email = input("Ingrese email: ")

    if not re.match(r'^\d{10}$', ci):
        print("CI inválida.")
        return

    try:
        conexion.insertar_cliente(ci, nombre, email)
        print("Cliente insertado correctamente.")
    except Exception as e:
        print("Error:", e)


def eliminar_cliente():
    try:
        id_cliente = int(input("Ingrese ID: "))
        filas = conexion.eliminar_cliente(id_cliente)

        if filas > 0:
            print("Cliente eliminado.")
        else:
            print("No existe ese cliente.")

    except ValueError:
        print("Debe ingresar un número válido.")


def actualizar_cliente():
    try:
        id_cliente = int(input("Ingrese ID del cliente: "))
        nuevo_email = input("Ingrese nuevo email: ")

        filas = conexion.actualizar_cliente(id_cliente, nuevo_email)

        if filas > 0:
            print("Cliente actualizado.")
        else:
            print("No existe ese cliente.")
    except ValueError:
        print("Debe ingresar un número válido.")
    except Exception as e:
        print("Debe ingresar un formato valido")



def menu_consultas():
    while True:
        print("""
        1. Top 3 clientes con más pedidos
        2. Demanda de platos
        3. Pedidos en Febrero y Marzo
        4. Ingresos por tipo de pago
        5. Volver
        """)

        op = input("Seleccione: ")

        if op == "1":
            print("Top 3 clientes con más pedidos")
            print("  " + "-" * 40)
            for nombre, total in conexion.top3_clientes():
                print(f"  {nombre:20} | pedidos: {total}")

        elif op == "2":
            print("Demanda de platos")
            print("  " + "-" * 50)
            for plato, vendidos in conexion.demanda_platos():
                print(f"  {plato:25} | total vendido: {vendidos}")

        elif op == "3":
            print("Pedidos en Febrero y Marzo")
            print(f"  {'id':<4} {'CI':<12} {'cliente':<15} {'email':<25} {'fecha':<20} {'cantidad':<10} {'plato':<20} {'servido'}")
            print("  " + "-" * 130)
            for fila in conexion.pedidos_febrero_marzo():
                id_ord, ci, nombre, email, dt, cantidad, plato, servido = fila
                date_str = dt.strftime('%Y-%m-%d %H:%M:%S') if hasattr(dt, 'strftime') else str(dt)
                print(f"  {id_ord:<4} {ci:<12} {nombre:<15} {email:<25} {date_str:<20} {cantidad:<10} {plato:<20} {servido}")

        elif op == "4":
            print("Ingresos por tipo de pago")
            print("  " + "-" * 40)
            for tipo, ingreso in conexion.ingresos_por_tipo_pago():
                print(f"  {tipo:15} | ingreso: {ingreso}")

        elif op == "5":
            break

        else:
            print("Opción inválida.")


def menu():
    while True:
        imprimir_menu()

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_clientes()
        elif opcion == "2":
            ingresar_cliente()
        elif opcion == "3":
            eliminar_cliente()
        elif opcion == "4":
            actualizar_cliente()
        elif opcion == "5":
            menu_consultas()
        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

        # pausa después de procesar la opción (siempre se ejecuta)
        input("\nPresione Enter para continuar...")  

        

if __name__ == "__main__":
    menu()