import pymongo

class Bienes:

    def __init__(self, placa, nombreBien, categoria, descripcion, estado):
        self.placa = placa
        self.nombreBien = nombreBien
        self.categoria = categoria
        self.descripcion = descripcion
        self.estado = estado

    def guardar(self):
        estado=0
        #abrir la conexión mediante un objeto cliente
        bien= pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        #seleccionar la tabla a utilizar
        bd=bien["TresPatitos"]
        try:
            #definir la tabla a utilizar
            tbl=bd["bienes"]
            #crear diccionario
            doc={"_placa":self.placa,
                "nombre":self.nombreBien,
                "categoria":self.categoria,
                "descripcion":self.descripcion}
            #insertar en la tabla
            tbl.insert_one(doc)
            estado=1
        except Exception:
            print("Error al guardar")
            estado=0
        finally:
            bien.close        
        return estado

    def actualizar(self):
        estado = 0
        # abrir la conexión mediante un objeto cliente
        bien = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        # seleccionar la tabla a utilizar
        bd = bien["empresa"]
        try:
            # definir la tabla a utilizar
            tbl = bd["bienes"]
            # filtro
            filtro = {"_placa": self.placa}
            # crear diccionario
            doc = {
                "$set": {
                    "nombre bien": self.nombreBien,
                    "categoria": self.categoria,
                    "descripcion": self.descripcion,
                    "estado": self.estado
                }
            }
            # modifcar en la tabla
            tbl.update_one(filtro,doc)
            estado = 1
        except Exception:
            print("Error al modificar")
            estado = 0
        finally:
            bien.close
        return estado

    def eliminar(self):
        estado = 0
        # abrir la conexión mediante un objeto cliente
        bien = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        # seleccionar la tabla a utilizar
        bd = bien["empresa"]
        try:
            # definir la tabla a utilizar
            tbl = bd["bienes"]
            # filtro
            filtro = {"_placa": self.placa}
            # modifcar en la tabla
            tbl.delete_one(filtro)
            estado = 1
        except Exception:
            print("Error al eliminar")
            estado = 0
        finally:
            bien.close
        return estado