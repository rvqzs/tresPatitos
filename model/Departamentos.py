import pymongo

class Departamentos:
    
    def __init__(self, codigo, nombre, jefatura):
        self.codigo = codigo
        self.nombre = nombre
        self.jefatura = jefatura

    def registrar(self):
        estado=0
        departamento= pymongo.MongoClient("mongodb://localhost:27017")
        #seleccionar la tabla a utilizar
        bd=departamento["Empresa"]
        try:
            #definir la tabla a utilizar
            tbl=bd["departamentos"]
            #crear diccionario
            doc={"_codigo":self.codigo,
                "nombre":self.nombre,
                "jefatura":self.jefatura}
            #insertar en la tabla
            tbl.insert_one(doc)
            estado=1
        except Exception:
            print("Error al guardar")
            estado=0
        finally:
            departamento.close        
        return estado

    def actualizar(self):
        estado = 0
        departamento = pymongo.MongoClient("mongodb://localhost:27017")
        bd = departamento["Empresa"]
        try:
            # definir la tabla a utilizar
            tbl = bd["bien"]
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
        bd = bien["bien"]
        try:
            # definir la tabla a utilizar
            tbl = bd["bien"]
            # filtro
            filtro = {"_placa": self.placa}
            # modifcar en la tabla
            tbl.delete_one(filtro)
            estado = 1
        except Exception:
            print("error al eliminar")
            estado = 0
        finally:
            bien.close
        return estado