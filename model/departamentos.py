import pymongo

class Departamentos:
    
    def __init__(self, codigo=1, nombre=2, jefatura=3):
        self.codigo = codigo
        self.nombre = nombre
        self.jefatura = jefatura

    def registrar(self):
        departamento = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = departamento["TresPatitos"]
        try:
            tbl = bd["departamentos"]
            doc ={
            "_id": self.codigo,
            "nombre": self.nombre,
            "jefatura":self.jefatura
            }
            tbl.insert_one(doc)
            estado = 1
        except Exception:
            print("Error al guardar")
            estado = 0
        finally:
            departamento.close
        return estado

    def actualizar(self):
        departamento = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = departamento["TresPatitos"]
        try:
            tbl = bd["departamentos"]
            filtro = {"_id": self.codigo}
            doc={"$set":
                {"_id":self.codigo,
                "nombre":self.nombre,
                "jefatura":self.jefatura
                }
                }
            
            tbl.update_one(filtro,doc)
            estado = 1
        except Exception as e:
            print("Error al modificar", e)
            estado = 0
        finally:
            departamento.close
        return estado

    def eliminar(self):
        departamento = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = departamento["TresPatitos"]
        try:
            tbl = bd["departamentos"]
            filtro = {"_id": self.codigo}
            tbl.delete_one(filtro)
            estado = 1
        except Exception as e:
            print("Error al eliminar", e)
            estado = 0
        finally:
            departamento.close
        return estado
    
    def existeDepartamento(self, nombre_departamento):
        departamento = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = departamento["TresPatitos"]
        try:
            tbl = bd["departamentos"]
            filtro = {"nombre": nombre_departamento}  # Use the provided department name
            resultado = tbl.find_one(filtro)
            if resultado is not None:
                return True
        except Exception as e:
            print("Error al verificar si existe el departamento:", e)
            return False
        finally:
            departamento.close()
        
    def getDepartamentos(self):
        usuarios=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=usuarios["TresPatitos"]
        tbl=bd["departamentos"]
        return tbl.find()
    
    def getCountDepartamentos(self):
        usuarios=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=usuarios["TresPatitos"]
        size=bd.command("collstats","departamentos") #estadisticas
        return size["count"]

    def getLastCode(self):
        cliente = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        db = cliente["TresPatitos"]
        ultimo_departamento = db["departamentos"].find().sort("_id", pymongo.DESCENDING).limit(1)
        count = db["departamentos"].count_documents({})
        if count > 0:
            self.ultimo_codigo = ultimo_departamento[0]["_id"]
            self.ultimo_numero = int(self.ultimo_codigo[3:])
        else:
            self.ultimo_numero = 0
        return self.ultimo_numero
