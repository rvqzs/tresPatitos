import pymongo

class ReporteBienesAsignados:
    def __init__(self):
        pass

    def getAsignados(self):
        bienAsignado = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = bienAsignado["TresPatitos"]
        tbl = bd["bienes_asignados"]
        return tbl.find()

    def getNumeroAsignadosReporte(self):
        bienAsignado = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = bienAsignado["TresPatitos"]
        size=bd.command("collstats","bienes_asignados")
        return size["count"]