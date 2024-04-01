import pymongo

class DesligarBienes:
    def __init__(self):
        pass

    def getAsignados(self):
        bienAsignado = pymongo.MongoClient("mongodb+srv://admin:admin@trespatitosdb.mi0zzv0.mongodb.net/")
        bd = bienAsignado["TresPatitos"]
        tbl = bd["bienes_asignados"]
        return tbl.find()