import numpy as np


class Table:

    def __init__(self, rows, cols):
        self.innerTable = np.chararray((rows,cols), itemsize=10)
        self.numRows = rows
        self.indexOfIndex = -1
        self.colNames = []

    def setIndex(index):
        self.indexOfIndex = index

    def setColNames(col_names):
        for col_name in col_names:
            self.colNames.append(col_name)
