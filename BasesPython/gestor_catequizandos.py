import pyodbc
import json

class GestorCatequizandos:
    """
    Clase que encapsula la conexión y las operaciones CRUD
    para la tabla Catequizando, utilizando Store Procedures de SQL Server.
    """
    def __init__(self):
        """
        Inicializa la conexión a la base de datos leyendo credenciales
        desde 'config.json'.
        """
        try:
            with open('config.json', 'r') as archivo_config:
                config = json.load(archivo_config)

            servidor = config['server']
            base_datos = config['database']
            usuario = config['user']
            clave = config['password']

            # La conexión se almacena en self.conexion (encapsulamiento)
            self.conexion = pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={servidor};DATABASE={base_datos};UID={usuario};PWD={clave}'
            )
            print("Conexión exitosa a la base de datos.")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.conexion = None


# --- MÉTODOS CRUD

    def insertar(self, documento_id, nombres, apellidos, fecha_nacimiento,
                 telefono=None, email=None, direccion=None,
                 representante_nombre=None, representante_email=None,
                 representante_telefono=None, bautizo_fecha=None, padrinos=None):
        """Llama a academico.SP_Catequizando_Insert."""
        if not self.conexion: return
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                EXEC academico.SP_Catequizando_Insert 
                    @Documento_id=?, @Nombres=?, @Apellidos=?, @Fecha_nacimiento=?,
                    @Telefono=?, @Email=?, @Direccion=?, 
                    @Representante_nombre=?, @Representante_email=?, @Representante_telefono=?,
                    @Bautizo_fecha=?, @Padrinos=?
            """, (documento_id, nombres, apellidos, fecha_nacimiento,
                  telefono, email, direccion,
                  representante_nombre, representante_email, representante_telefono,
                  bautizo_fecha, padrinos))
            self.conexion.commit()
            print("Registro insertado correctamente.")
        except Exception as e:
            print(f"Error al insertar: {e}")

    def consultar_por_id(self, id_catequizando):
        """Llama a academico.SP_Catequizando_GetById."""
        if not self.conexion: return
        try:
            cursor = self.conexion.cursor()
            cursor.execute("EXEC academico.SP_Catequizando_GetById @Id=?", id_catequizando)
            fila = cursor.fetchone()
            if fila:
                print("\nRegistro encontrado:")
                print(fila)
            else:
                print("No se encontró ningún catequizando con ese ID.")
        except Exception as e:
            print(f"Error al consultar por ID: {e}")

    def consultar_todos(self):
        """Llama a academico.SP_Catequizando_GetAll."""
        if not self.conexion: return
        try:
            cursor = self.conexion.cursor()
            cursor.execute("EXEC academico.SP_Catequizando_GetAll")
            registros = cursor.fetchall()
            print("\nLISTADO DE CATEQUIZANDOS:")
            if registros:
                for fila in registros:
                    print(fila)
            else:
                print("No hay registros para mostrar.")
        except Exception as e:
            print(f"Error al consultar todos: {e}")

    def actualizar(self, id_catequizando, documento_id, nombres, apellidos, fecha_nacimiento,
                   telefono=None, email=None, direccion=None,
                   representante_nombre=None, representante_email=None,
                   representante_telefono=None, bautizo_fecha=None, padrinos=None):
        """Llama a academico.SP_Catequizando_Update."""
        if not self.conexion: return
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                EXEC academico.SP_Catequizando_Update 
                    @Id=?, @Documento_id=?, @Nombres=?, @Apellidos=?, @Fecha_nacimiento=?,
                    @Telefono=?, @Email=?, @Direccion=?, 
                    @Representante_nombre=?, @Representante_email=?, @Representante_telefono=?,
                    @Bautizo_fecha=?, @Padrinos=?
            """, (id_catequizando, documento_id, nombres, apellidos, fecha_nacimiento,
                  telefono, email, direccion,
                  representante_nombre, representante_email, representante_telefono,
                  bautizo_fecha, padrinos))
            self.conexion.commit()
            print("Registro actualizado correctamente.")
        except Exception as e:
            print(f"Error al actualizar: {e}")

    def eliminar(self, id_catequizando):
        """Llama a academico.SP_Catequizando_Delete."""
        if not self.conexion: return
        try:
            cursor = self.conexion.cursor()
            cursor.execute("EXEC academico.SP_Catequizando_Delete @Id=?", id_catequizando)
            self.conexion.commit()
            print("Registro eliminado correctamente.")
        except Exception as e:
            print(f"Error al eliminar: {e}")


# --- METODO ejecutar_menu()


    def ejecutar_menu(self):
        """Muestra el menú CRUD y llama a los métodos de la clase usando input()."""
        if not self.conexion:
            print("No se puede ejecutar el menú sin una conexión a la base de datos.")
            return

        while True:
            print("\n\t** SISTEMA CRUD UDEMYTEST **")
            print("\t1. Crear registro (Insertar)")
            print("\t2. Consultar por ID")
            print("\t3. Listar todos")
            print("\t4. Actualizar registro")
            print("\t5. Eliminar registro")
            print("\t6. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                # Insertar
                print("\n--- INGRESO DE NUEVO CATEQUIZANDO ---")
                try:
                    doc = input("Documento ID: ")
                    nom = input("Nombres: ")
                    ape = input("Apellidos: ")
                    fecha = input("Fecha de nacimiento (YYYY-MM-DD): ")
                    self.insertar(doc, nom, ape, fecha)
                except Exception:
                    print("Error en el formato de los datos ingresados.")

            elif opcion == '2':
                # Consultar por ID
                try:
                    idc = int(input("Ingrese el ID del catequizando a consultar: "))
                    self.consultar_por_id(idc)
                except ValueError:
                    print("El ID debe ser un número entero.")

            elif opcion == '3':
                # Listar todos
                self.consultar_todos()

            elif opcion == '4':
                # Actualizar
                print("\n--- ACTUALIZACION DE CATEQUIZANDO (Solo datos basicos) ---")
                try:
                    idc = int(input("Ingrese el ID del catequizando a actualizar: "))
                    doc = input("Nuevo Documento ID: ")
                    nom = input("Nuevos Nombres: ")
                    ape = input("Nuevos Apellidos: ")
                    fecha = input("Nueva Fecha de nacimiento (YYYY-MM-DD): ")
                    # Llama al metodo de la clase con los parametros de INPUT
                    self.actualizar(idc, doc, nom, ape, fecha)
                except ValueError:
                    print("El ID debe ser un número entero.")

            elif opcion == '5':
                # Eliminar
                try:
                    idc = int(input("Ingrese el ID del catequizando a eliminar: "))
                    self.eliminar(idc)
                except ValueError:
                    print("El ID debe ser un número entero.")

            elif opcion == '6':
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")




