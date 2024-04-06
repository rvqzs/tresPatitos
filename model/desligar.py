import pymongo

class DesligarBienes:
    def __init__(self, cedula=1, nombre=2):
        self.cedula=cedula
        self.nombre=nombre

    def eliminar(self):
        estado = 0
        # abrir la conexión mediante un objeto cliente
        bienAsignado = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        # seleccionar la tabla a utilizar
        bd = bienAsignado["TresPatitos"]
        try:
            # definir la tabla a utilizar
            tbl = bd["bienes_asignados"]
            elemento = tbl ["nombre"]
            # filtro
            filtro = {"_id": self.cedula}
            # modifcar en la tabla
            elemento.delete_many(filtro)
            estado = 1
        except Exception:
            print("Error al eliminar")
            estado = 0
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
            filtro = {"_id": self.cedula}
            # crear diccionario
            doc = {
                "$set": {
                    "bien_asignado": "No Asignado"
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

    def getAsignados(self):
        bienAsignado = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = bienAsignado["TresPatitos"]
        tbl = bd["bienes_asignados"]
        return tbl.find()
    
    def getNumeroDesligar(self):
        bienDesligar = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = bienDesligar["TresPatitos"]
        size=bd.command("collstats","bienes_asignados")
        return size["count"]