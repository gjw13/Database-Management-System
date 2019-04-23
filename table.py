import numpy as np


class Table:

    def __init__(self, rows, cols):
        self.relation = np.chararray((rows,cols), itemsize=10)
        self.name = ""
        self.numRows = rows
        self.numCols = cols
        self.indices = []
        self.colNames = []

    def setName(self,table_name):
        self.name = table_name.upper()

    def addIndex(indexName, col_name, ordering):
        i = 0
        col_index = -1
<<<<<<< HEAD
        while i < len(colNames):
            if col_name == colNames[i]:
=======
        while i < self.numCols:
            if col_name == self.colNames[i]:
>>>>>>> 8c5ebb5f578045e86861d66ce87060076e3f31c1
                col_index = i
                i = len(colNames)
        self.indices.append((indexName, col_index, ordering))

    def setColNames(col_names):
        for col_name in col_names:
            self.colNames.append(col_name)
