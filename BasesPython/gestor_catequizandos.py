import pyodbc
import json
import re
from datetime import datetime

class GestorCatequizandos:
    def __init__(self):
        try:
            with open('config.json', 'r') as archivo_config:
                config = json.load(archivo_config)

            servidor = config['server']
            base_datos = config['database']
            usuario = config['user']
            clave = config['password']

            self.conexion = pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={servidor};DATABASE={base_datos};UID={usuario};PWD={clave}'
            )
            print("✅ Conexión exitosa a la base de datos.")
        except Exception as e:
            print(f"❌ Error al conectar a la base de datos: {e}")
            self.conexion = None

    def validar_documento(self, documento_id):
        return bool(documento_id and documento_id.strip())

    def validar_fecha(self, fecha_texto):
        try:
            datetime.strptime(fecha_texto, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def validar_email(self, email):
        if not email:
            return True
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(patron, email) is not None

    def insertar(self, documento_id, nombres, apellidos, fecha_nacimiento,
                 telefono=None, email=None, direccion=None,
                 representante_nombre=None, representante_email=None,
                 representante_telefono=None, bautizo_fecha=None, padrinos=None):

        if not self.validar_documento(documento_id):
            print("⚠️ El campo Documento no puede estar vacío.")
            return
        if not self.validar_fecha(fecha_nacimiento):
            print("⚠️ La fecha debe tener formato YYYY-MM-DD.")
            return
        if not self.validar_email(email):
            print("⚠️ El email no es válido.")
            return

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
            print("✅ Registro insertado correctamente.")
        except pyodbc.IntegrityError:
            print("❌ Error: Documento duplicado o restricción de clave violada.")
        except pyodbc.DatabaseError as e:
            print(f"❌ Error de base de datos: {e}")
        except Exception as e:
            print(f"⚠️ Error inesperado: {e}")

    def consultar_por_id(self, id_catequizando):
        if not self.conexion:
            return
        try:
            cursor = self.conexion.cursor()
            cursor.execute("EXEC academico.SP_Catequizando_GetById @Id=?", id_catequizando)
            fila = cursor.fetchone()
            if fila:
                print("\nRegistro encontrado:")
                print(fila)
            else:
                print("⚠️ No se encontró ningún catequizando con ese ID.")
        except Exception as e:
            print(f"❌ Error al consultar por ID: {e}")

    def consultar_todos(self):
        if not self.conexion:
            return
        try:
            cursor = self.conexion.cursor()
            cursor.execute("EXEC academico.SP_Catequizando_GetAll")
            registros = cursor.fetchall()
            print("\n📋 LISTADO DE CATEQUIZANDOS:")
            if registros:
                for fila in registros:
                    print(fila)
            else:
                print("⚠️ No hay registros para mostrar.")
        except Exception as e:
            print(f"❌ Error al consultar todos: {e}")

    def actualizar(self, id_catequizando, documento_id, nombres, apellidos, fecha_nacimiento,
                   telefono=None, email=None, direccion=None,
                   representante_nombre=None, representante_email=None,
                   representante_telefono=None, bautizo_fecha=None, padrinos=None):

        if not self.validar_documento(documento_id):
            print("⚠️ El campo Documento no puede estar vacío.")
            return
        if not self.validar_fecha(fecha_nacimiento):
            print("⚠️ La fecha debe tener formato YYYY-MM-DD.")
            return
        if not self.validar_email(email):
            print("⚠️ El email no es válido.")
            return

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
            print("✅ Registro actualizado correctamente.")
        except pyodbc.DatabaseError as e:
            print(f"❌ Error de base de datos: {e}")
        except Exception as e:
            print(f"⚠️ Error inesperado: {e}")

    def eliminar(self, id_catequizando):
        if not self.conexion:
            return
        try:
            cursor = self.conexion.cursor()
            cursor.execute("EXEC academico.SP_Catequizando_Delete @Id=?", id_catequizando)
            self.conexion.commit()
            print("✅ Registro eliminado correctamente.")
        except pyodbc.DatabaseError as e:
            print(f"❌ Error de base de datos: {e}")
        except Exception as e:
            print(f"⚠️ Error inesperado: {e}")

    def ejecutar_menu(self):
        if not self.conexion:
            print("❌ No se puede ejecutar el menú sin una conexión a la base de datos.")
            return

        while True:
            print("\n\t** SISTEMA CRUD CATEQUIZANDOS **")
            print("\t1. Crear registro (Insertar)")
            print("\t2. Consultar por ID")
            print("\t3. Listar todos")
            print("\t4. Actualizar registro")
            print("\t5. Eliminar registro")
            print("\t6. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                print("\n--- INGRESO DE NUEVO CATEQUIZANDO ---")
                doc = input("Documento ID: ")
                nom = input("Nombres: ")
                ape = input("Apellidos: ")
                fecha = input("Fecha de nacimiento (YYYY-MM-DD): ")
                self.insertar(doc, nom, ape, fecha)

            elif opcion == '2':
                try:
                    idc = int(input("Ingrese el ID del catequizando a consultar: "))
                    self.consultar_por_id(idc)
                except ValueError:
                    print("⚠️ El ID debe ser un número entero.")

            elif opcion == '3':
                self.consultar_todos()

            elif opcion == '4':
                print("\n--- ACTUALIZACION DE CATEQUIZANDO ---")
                try:
                    idc = int(input("Ingrese el ID del catequizando a actualizar: "))
                    doc = input("Nuevo Documento ID: ")
                    nom = input("Nuevos Nombres: ")
                    ape = input("Nuevos Apellidos: ")
                    fecha = input("Nueva Fecha de nacimiento (YYYY-MM-DD): ")
                    self.actualizar(idc, doc, nom, ape, fecha)
                except ValueError:
                    print("⚠️ El ID debe ser un número entero.")

            elif opcion == '5':
                try:
                    idc = int(input("Ingrese el ID del catequizando a eliminar: "))
                    self.eliminar(idc)
                except ValueError:
                    print("⚠️ El ID debe ser un número entero.")

            elif opcion == '6':
                print("👋 Saliendo del sistema...")
                break
            else:
                print("⚠️ Opción inválida. Intente nuevamente.")
