import pymongo

class crearEmpleados:
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
        empleados=pymongo.MongoClient("mongodb://localhost:27017")
        bd=empleados["Empresa"]
        try:
            #definir la tabla a utilizar
            tbl=bd["Empleados"]
            #crear diccionario
            doc={"_id":self.cedula,"Nombre":self.nombre,"Apellidos":self.apellidos,"Telefono":self.telefono,"Direccion":self.direccion,"Puesto":self.puesto,"Ingreso":self.ingreso,"Jefatura":self.jefatura}
            #insertar en la tabla
            tbl.insert_one(doc)
            estado=1
        except Exception:
            print("error al guardar")
            estado=0
        finally:
            empleados.close
        return estado