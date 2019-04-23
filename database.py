import numpy as np

class Database:

    def __init__(self):
        self.relationList = []
        self.numRelations = 0

    def addRelation(self,relation):
        self.relationList.append(relation)
        self.numRelations += 1
