# evaluator functions
# helpers
import numpy as np

def eval_select(cols, tables, conditions):
    print("IN EVAL")
    return 0

def eval_create_table(table_name,cols):
    num_cols = len(cols)+1
    test = np.chararray((num_cols,num_cols),itemsize=10)
    test.fill('null')
    np.put(test, 0, table_name)
    np.put(test, 1,cols[0])
    np.put(test, 2,cols[1])
    np.put(test, 3,"greg")
    # test[0:1] = table_name
    print(test)

eval_create_table("customers",("first","last"))
