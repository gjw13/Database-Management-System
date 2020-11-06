import numpy as np


class Table:
    def __init__(self, rows, cols):
        self.relation = np.chararray((rows, cols), itemsize=10)
        self.name = "placeholder"
        self.numRows = rows
        self.numCols = cols
        self.indices = []
        self.colNames = []

    def setName(self, table_name):
        self.name = table_name.upper()

    def addIndex(self, indexName, col_name, ordering):
        self.indices.append((indexName, col_name, ordering))

    def setColNames(self, col_names):
        for col_name in col_names:
            self.colNames.append(col_name)

    def getColNames(self):
        index_of_cols = []
        for x in range(0, self.numCols):
            index_of_cols.append(x)
        columns = np.take(self.relation, index_of_cols)
        self.colNames = columns[:].tolist()
        return columns

    def columnExists(self, col_name):
        return col_name in self.colNames

    def setNumCols(self, numCols):
        self.numCols = numCols

    def setNumRows(self, numRows):
        self.numRows = numRows

    def getIndicies(self):
        return self.indices
