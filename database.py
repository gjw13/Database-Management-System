import numpy as np

class Database:

    def __init__(self):
        self.relationList = []
        self.numRelations = 0

    def addRelation(self,relation):
        self.relationList.append(relation)
        self.numRelations += 1

    def getRelation(self,table_name):
        for relation in self.relationList:
            if relation.name == table_name.upper():
                return relation

    def tableExists(self,table_name):
        for relation in self.relationList:
            if relation.name == table_name.upper():
                return True
        return False

    def removeRelation(self, relation):
        if self.tableExists(relation.name):
            self.relationList.remove(relation)
            self.numRelations -= 1
