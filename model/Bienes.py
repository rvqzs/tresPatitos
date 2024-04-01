import pymongo


class Bienes:
    def __init__(self, placa=1, nombreBien=2, categoria=3, descripcion=4, estado=5):
        self.placa = placa
        self.nombreBien = nombreBien
        self.categoria = categoria
        self.descripcion = descripcion
        self.estado = estado

    def guardar(self):
        estado=0
        #abrir la conexión mediante un objeto cliente
        bien= pymongo.MongoClient("mongodb://localhost:27017")
        #seleccionar la tabla a utilizar
        bd=bien["Empresa"]
        try:
            #definir la tabla a utilizar
            tbl=bd["bienes"]
            #crear diccionario
            doc={"_id":self.placa,
                "nombre bien":self.nombreBien,
                "categoria":self.categoria,
                "descripcion":self.descripcion,
                "estado": self.estado}
            #insertar en la tabla
            tbl.insert_one(doc)
            estado=1
        except Exception:
            print("error al guardar")
            estado=0
        finally:
            bien.close        
        return estado

    def actualizar(self):
        estado = 0
        # abrir la conexión mediante un objeto cliente
        bien = pymongo.MongoClient("mongodb://localhost:27017")
        # seleccionar la tabla a utilizar
        bd = bien["Empresa"]
        try:
            # definir la tabla a utilizar
            tbl = bd["bienes"]
            # filtro
            filtro = {"_id": self.placa}
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
            print("error al modificar")
            estado = 0
        finally:
            bien.close
        return estado

    def eliminar(self):
        estado = 0
        # abrir la conexión mediante un objeto cliente
        bien = pymongo.MongoClient("mongodb://localhost:27017")
        # seleccionar la tabla a utilizar
        bd = bien["Empresa"]
        try:
            # definir la tabla a utilizar
            tbl = bd["bienes"]
            # filtro
            filtro = {"_id": self.placa}
            # modifcar en la tabla
            tbl.delete_one(filtro)
            estado = 1
        except Exception:
            print("error al eliminar")
            estado = 0
        finally:
            bien.close
        return estado
    
    def getBienes(self):
        bien = pymongo.MongoClient("mongodb://localhost:27017")
        bd = bien["Empresa"]
        tbl = bd["bienes"]
        return tbl.find()

    def getNumeroRegistros(self):
        bien = pymongo.MongoClient("mongodb://localhost:27017")
        bd = bien["Empresa"]
        size=bd.command("collstats","bienes")
        return size["count"]