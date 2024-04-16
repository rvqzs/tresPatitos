import pymongo

class Usuarios:

    def __init__(self, username=1, name=2, password=3, is_admin=4):
        self.username = username
        self.name = name
        self.password = password
        self.admin = is_admin

    def guardar(self):
        usuarios=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=usuarios["TresPatitos"]
        try:
            tbl=bd["usuarios"]
            doc={
                "_id":self.username,
                "nombre":self.name,
                "password":self.password,
                "is_admin":self.admin
                }
            
            tbl.insert_one(doc)
            estado=1
        except Exception as e:
            if e=="E11000 duplicate key error collection:":
                print("Error al guardar, el usuario ya está registrado")
                estado=0
            else:
                estado=2
        finally:
            usuarios.close
        return estado
    
    def actualizar(self):
        usuarios=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=usuarios["TresPatitos"]
        try:
            tbl=bd["usuarios"]
            filtro={"_id":self.username}
            doc={"$set":{"_id":self.username,
                "nombre":self.name,
                "password":self.password,
                "is_admin":self.admin
                }}
        
            tbl.update_one(filtro,doc)
            estado=1
        except Exception as e:
            print("Error al guardar", e)
            estado=0
        finally:
            usuarios.close
        return estado
    
    def eliminar(self):
        usuarios=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=usuarios["TresPatitos"]
        try:
            tbl=bd["usuarios"]
            filtro={"_id":self.username}
            tbl.delete_one(filtro)
            estado=1
        except Exception as e:
            print("Error al Eliminar", e)
            estado=0
        finally:
            usuarios.close
        return estado
    
    def getUsuarios(self):
        usuarios=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=usuarios["TresPatitos"]
        tbl=bd["usuarios"]
        return tbl.find()
    
    def getRegistrosUsuarios(self):
        usuarios=pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd=usuarios["TresPatitos"]
        size=bd.command("collstats","usuarios")
        return size["count"]

    def validarUsuarios(self, username, password):
        client = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        db = client["TresPatitos"]
        collection = db["usuarios"]
        user = collection.find_one({"_id": username, "password": password})

        if user:
            # Assuming the "admin" field indicates whether the user is an admin
            is_admin = user.get("admin", False)
            return True, is_admin
        else:
            return False, False

