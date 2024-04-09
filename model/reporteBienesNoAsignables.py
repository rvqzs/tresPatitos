import pymongo

class ReporteBienesNoAsignables:
    def __init__(self, placa=1, nombreBien=2, categoria=3, descripcion=4, estado=5):
        self.placa = placa
        self.nombreBien = nombreBien
        self.categoria = categoria
        self.descripcion = descripcion
        self.estado = estado

    def getBienes(self):
        bien = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = bien["TresPatitos"]
        tbl = bd["bienes"]
        return tbl.find()

    def getNumeroRegistros(self):
        bien = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = bien["TresPatitos"]
        size=bd.command("collstats","bienes")
        return size["count"]