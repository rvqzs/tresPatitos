import pymongo


class AsignarBienes:
    def __init__(self, cedula=1, nombre=2, telefono=3, bienAsignado=4):
        self.cedula = cedula
        self.nombre = nombre
        self.telefono = telefono
        self.bienAsignado = bienAsignado

    def guardar(self):
        estado=0
        #abrir la conexión mediante un objeto cliente
        bienAsignado= pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        #seleccionar la tabla a utilizar
        bd=bienAsignado["TresPatitos"]
        try:
            #definir la tabla a utilizar
            tbl=bd["bienes_asignados"]
            #crear diccionario
            doc={"cedula":self.cedula,
                "nombre":self.nombre,
                "telefono":self.telefono,
                "_id": self.bienAsignado}
            #insertar en la tabla
            tbl.insert_one(doc)
            estado=1
        except Exception:
            print("Error al guardar")
            estado=0
        finally:
            bienAsignado.close        
        return estado

    def actualizar(self):
        estado = 0
        # abrir la conexión mediante un objeto cliente
        bienAsignado = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        # seleccionar la tabla a utilizar
        bd = bienAsignado["TresPatitos"]
        try:
            # definir la tabla a utilizar
            tbl = bd["bienes_asignados"]
            # filtro
            filtro = {"cedula": self.cedula}
            # crear diccionario
            doc = {
                "$set": {
                    "nombre": self.nombre,
                    "telefono": self.telefono,
                    "bien_asignado": self.bienAsignado
                }
            }
            # modifcar en la tabla
            tbl.update_one(filtro,doc)
            estado = 1
        except Exception:
            print("Error al modificar")
            estado = 0
        finally:
            bienAsignado.close
        return estado

    def eliminar(self):
        estado = 0
        # abrir la conexión mediante un objeto cliente
        bienAsignado = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        # seleccionar la tabla a utilizar
        bd = bienAsignado["TresPatitos"]
        try:
            # definir la tabla a utilizar
            tbl = bd["bienes_asignados"]
            # filtro
            filtro = {"cedula": self.cedula}
            # modifcar en la tabla
            tbl.delete_one(filtro)
            estado = 1
        except Exception:
            print("Error al eliminar")
            estado = 0
        finally:
            bienAsignado.close
        return estado
    
    def getAsignados(self):
        bienAsignado = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = bienAsignado["TresPatitos"]
        tbl = bd["bienes_asignados"]
        return tbl.find()

    def getNumeroAsignados(self):
        bienAsignado = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = bienAsignado["TresPatitos"]
        size=bd.command("collstats","bienes_asignados")
        return size["count"]
    
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
    
    def getBienes(self):
        bien = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = bien["TresPatitos"]
        tbl = bd["bienes"]
        bienes_asignables = tbl.find({"estado": "Asignable"})
        return bienes_asignables

    def getNumeroRegistros(self):
        bien = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = bien["TresPatitos"]
        size=bd.command("collstats","bienes")
        return size["count"]
