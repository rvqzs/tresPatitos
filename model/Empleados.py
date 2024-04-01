import pymongo

class empleados:
    def __init__(self,cedula=0, nombre=1, telefono=2,apellidos=3,direccion=4,puesto=5,ingreso=6,jefatura=7):
        self.cedula = cedula
        self.nombre = nombre
        self.apellidos = apellidos
        self.telefono = telefono
        self.direccion= direccion
        self.puesto=puesto
        self.ingreso=ingreso
        self.jefatura=jefatura

    def guardarempleados(self):
        empleados=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=empleados["TresPatitos"]
        try:
            #definir la tabla a utilizar
            tbl=bd["empleados"]
            #crear diccionario
            doc={"_id":self.cedula,
                "Nombre":self.nombre,
                "Apellidos":self.apellidos,
                "Telefono":self.telefono,
                "Direccion":self.direccion,
                "Puesto":self.puesto,
                "Ingreso":self.ingreso,
                "Jefatura":self.jefatura
                }
            #insertar en la tabla
            tbl.insert_one(doc)
            estado=1
        except Exception:
            print("Error al guardar")
            estado=0
        finally:
            empleados.close
        return estado
    
    def actualizarempleados(self):
        #abrir la conxion mediante un objeto cliente
        empleados=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=empleados["TresPatitos"]
        try:
            #definir la tabla a utilizar
            tbl=bd["empleados"]
            #filtro sirve para ver que quiero modificar
            filtro={"_id":self.cedula}
            #crear diccionario
            doc={"$set":{"Nombre":self.nombre,
                        "Apellidos":self.apellidos,
                        "Telefono":self.telefono,
                        "Direccion":self.direccion,
                        "Puesto":self.puesto,
                        "Ingreso":self.ingreso,
                        "Jefatura":self.jefatura}
                        }
            #insertar en la tabla
            tbl.update_one(filtro,doc)
            estado=1
        except Exception:
            print("Error al guardar")
            estado=0
        finally:
            empleados.close
        return estado
    
    def eliminarempleados(self):
        empleados=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=empleados["TresPatitos"]
        try:
            #definir la tabla a utilizar
            tbl=bd["empleados"]
            #filtro sirve para ver que quiero modificar
            filtro={"_id":self.cedula}
            tbl.delete_one(filtro)
            estado=1
        except Exception:
            print("Error al Eliminar")
            estado=0
        finally:
            empleados.close
        return estado
    
    def getempleados(self):
        empleados=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=empleados["TresPatitos"]
        tbl=bd["empleados"]
        return tbl.find()
    
    def getRegistrosEmpleados(self):
        empleados=pymongo.MongoClient("mongodb://localhost:27017")
        bd=empleados["TresPatitos"]
        size=bd.command("collstats","Empleados")
        return size["count"]

