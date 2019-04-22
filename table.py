import numpy as np


class Table:

    def __init__(self, rows, cols):
        self.innerTable = np.chararray((rows,cols), itemsize=10)
        self.numRows = rows
        self.indices = []
        self.colNames = []

    def addIndex(indexName, col_name, ordering):
        i = 0
        col_index = -1
        while i < len(colNames):
            if col_name == colNames[i]:
                col_index = i
                i = len(colNames)
        self.indices.append((indexName, col_index, ordering))

    def setColNames(col_names):
        for col_name in col_names:
            self.colNames.append(col_name)
