import pymongo

class Empleados:
    def __init__(self,cedula=0, nombre=1, apellidos=2,telefono=3,direccion=4,departamento=5,ingreso=6,jefatura=7):
        self.cedula = cedula
        self.nombre = nombre
        self.apellidos = apellidos
        self.telefono = telefono
        self.direccion= direccion
        self.departamento=departamento
        self.ingreso=ingreso
        self.jefatura=jefatura

    def guardarEmpleados(self):
        empleados=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=empleados["TresPatitos"]
        
        try:
            #definir la tabla a utilizar
            tbl=bd["empleados"]
            #crear diccionario
            doc={"_id":self.cedula,
                "nombre":self.nombre,
                "apellidos":self.apellidos,
                "telefono":self.telefono,
                "direccion":self.direccion,
                "departamento":self.departamento,
                "ingreso":self.ingreso,
                "jefatura":self.jefatura
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
    
    def actualizarEmpleados(self):
        #abrir la conxion mediante un objeto cliente
        empleados=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=empleados["TresPatitos"]

        try:
            #definir la tabla a utilizar
            tbl=bd["empleados"]
            #filtro sirve para ver que quiero modificar
            filtro={"_id":self.cedula}
            #crear diccionario
            doc={"$set":{"nombre":self.nombre,
                        "apellidos":self.apellidos,
                        "telefono":self.telefono,
                        "direccion":self.direccion,
                        "departamento":self.departamento,
                        "ingreso":self.ingreso,
                        "jefatura":self.jefatura}
                        }
            #insertar en la tablaS
            tbl.update_one(filtro,doc)
            estado=1
        except Exception:
            print("Error al guardar")
            estado=0
        finally:
            empleados.close
        return estado
    
    def eliminarEmpleados(self):
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
    
    def getEmpleados(self):
        empleados=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=empleados["TresPatitos"]
        tbl=bd["empleados"]
        return tbl.find()
    
    def getRegistrosEmpleados(self):
        empleados=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=empleados["TresPatitos"]
        size=bd.command("collstats","empleados")
        return size["count"]
