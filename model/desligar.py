import pymongo

class DesligarBienes:
    def __init__(self):
        pass

    def getAsignados(self):
        bienAsignado = pymongo.MongoClient("mongodb://localhost:27017")
        bd = bienAsignado["Empresa"]
        tbl = bd["bienes_asignados"]
        return tbl.find()