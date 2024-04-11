import pymongo

class Empleados:
    def __init__(self, usuario=1, departamento =2, cedula=3, nombre=4, telefono=5,
                fechaIngreso=6, direccion=7, isJefatura=8):
        
        self.usuario=usuario
        self.cedula = cedula
        self.nombre = nombre
        self.telefono = telefono
        self.fechaIngreso=fechaIngreso
        self.direccion= direccion
        self.departamento=departamento
        self.isJefatura=isJefatura

    def guardarEmpleados(self):
        empleados=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=empleados["TresPatitos"]
        try:
            tbl=bd["empleados"]
            #crear diccionario
            doc={"_id":self.usuario,
                "departamento":self.departamento,
                "cedula":self.cedula,
                "nombre":self.nombre,
                "telefono":self.telefono,
                "fechaIngreso":self.fechaIngreso,
                "direccion":self.direccion,
                "isJefatura":self.isJefatura
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
        empleados=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=empleados["TresPatitos"]
        try:
            tbl=bd["empleados"]
            filtro={"_id":self.usuario}
            doc={"$set":
                {
                "departamento":self.departamento,
                "cedula":self.cedula,
                "nombre":self.nombre,
                "telefono":self.telefono,
                "fechaIngreso":self.fechaIngreso,
                "direccion":self.direccion,
                "isJefatura":self.isJefatura
                }
                }
            tbl.update_one(filtro,doc)
            estado=1
        except Exception:
            print("Error de actualización")
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
            filtro={"_id":self.usuario}
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
    
    def getJefaturas(self):
        jefaturas = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = jefaturas["TresPatitos"]
        tbl = bd["empleados"]
        return tbl.find({"isJefatura":True})
    
    def getRegistrosEmpleados(self):
        empleados=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=empleados["TresPatitos"]
        size=bd.command("collstats","empleados")
        return size["count"]
