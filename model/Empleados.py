import pymongo

class Empleados:
    def __init__(self,cedula, nombre, telefono,apellidos,direccion,puesto,ingreso,jefatura):
        self.cedula = cedula
        self.nombre = nombre
        self.apellidos = apellidos
        self.telefono = telefono
        self.direccion= direccion
        self.puesto=puesto
        self.ingreso=ingreso
        self.jefatura=jefatura

    def guardarEmpleados(self):
        empleados=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=empleados["TresPatitos"]
        try:
            #definir la tabla a utilizar
            tbl=bd["empleados"]
            #crear diccionario
            doc={"_id":self.cedula,"Nombre":self.nombre,
                "Apellidos":self.apellidos,"Telefono":self.telefono,
                "Direccion":self.direccion,"Puesto":self.puesto,"Ingreso":self.ingreso,
                "Jefatura":self.jefatura}
            #insertar en la tabla
            tbl.insert_one(doc)
            estado=1
        except Exception:
            print("Error al guardar")
            estado=0
        finally:
            empleados.close
        return estado