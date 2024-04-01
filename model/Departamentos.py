import pymongo

class Departamentos:
    
    def __init__(self, codigo, nombre, jefatura):
        self.codigo = codigo
        self.nombre = nombre
        self.jefatura = jefatura

    def registrar(self):
        estado=0
        departamento= pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        #seleccionar la tabla a utilizar
        bd=departamento["TresPatitos"]
        try:
            #definir la tabla a utilizar
            tbl=bd["departamentos"]
            #crear diccionario
            doc={"_id":self.codigo,
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
        departamento = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = departamento["TresPatitos"]
        try:
            tbl = bd["departamentos"]
            filtro = {"_id": self.codigo}
            doc={"_codigo":self.codigo,
                "nombre":self.nombre,
                "jefatura":self.jefatura
                }
            
            # modifcar en la tabla
            tbl.update_one(filtro,doc)
            estado = 1
        except Exception:
            print("Error al modificar")
            estado = 0
        finally:
            departamento.close
        return estado

    def eliminar(self):
        estado = 0
        departamento = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = departamento["TresPatitos"]
        try:
            # definir la tabla a utilizar
            tbl = bd["departamentos"]
            # filtro
            filtro = {"_id": self.codigo}
            # modifcar en la tabla
            tbl.delete_one(filtro)
            estado = 1
        except Exception:
            print("Error al eliminar")
            estado = 0
        finally:
            departamento.close
        return estado