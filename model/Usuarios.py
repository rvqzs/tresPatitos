import pymongo

class Usuarios:
    def __init__(self, id=1, nombreUsuario=2, email=3):
        self.id = id
        self.nombreUsuario = nombreUsuario
        self.email = email

        #self.telefono = telefono
        #self.direccion= direccion
        #self.puesto=puesto
        #self.ingreso=ingreso
        #self.jefatura=jefatura
    
    def guardar(self):
        #abrir la conxion mediante un objeto cliente
        usuarios=pymongo.MongoClient("mongodb://localhost:27017")
        bd=usuarios["Empresa"]
        try:
            #definir la tabla a utilizar
            tbl=bd["Usuarios"]
            #crear diccionario
            doc={"_id":self.id,"Usuario":self.nombreUsuario,"email":self.email}
            #insertar en la tabla
            tbl.insert_one(doc)
            estado=1
        except Exception:
            print("error al guardar")
            estado=0
        finally:
            usuarios.close
        return estado
    
    def actualizar(self):
        #abrir la conxion mediante un objeto cliente
        usuarios=pymongo.MongoClient("mongodb://localhost:27017")
        bd=usuarios["Empresa"]
        try:
            #definir la tabla a utilizar
            tbl=bd["Usuarios"]
            #filtro sirve para ver que quiero modificar
            filtro={"_id":self.id}
            #crear diccionario
            doc={"$set":{"Usuario":self.nombreUsuario,"email":self.email}}
            #insertar en la tabla
            tbl.update_one(filtro,doc)
            estado=1
        except Exception:
            print("error al guardar")
            estado=0
        finally:
            usuarios.close
        return estado
    
    def eliminar(self):
        usuarios=pymongo.MongoClient("mongodb://localhost:27017")
        bd=usuarios["Empresa"]
        try:
            #definir la tabla a utilizar
            tbl=bd["Usuarios"]
            #filtro sirve para ver que quiero modificar
            filtro={"_id":self.id}
            tbl.delete_one(filtro)
            estado=1
        except Exception:
            print("error al Eliminar")
            estado=0
        finally:
            usuarios.close
        return estado
    
    def getusuarios(self):
        usuarios=pymongo.MongoClient("mongodb://localhost:27017")
        bd=usuarios["Empresa"]
        tbl=bd["Usuarios"]
        return tbl.find()
    
    def getRegistrosUsuarios(self):
        usuarios=pymongo.MongoClient("mongodb://localhost:27017")
        bd=usuarios["Empresa"]
        size=bd.command("collstats","Usuarios")#estadisticas
        return size["count"]