# evaluator functions
# helpers
import numpy as np

def eval_select(cols, tables, conditions):
    # print("IN EVAL")
    table,num_cols,num_rows = eval_create_table("customers",("first","last","address"))
    columns = get_columns(table,num_cols)
    print(cols[0])
    if cols[0] != "*":
        # print("Not selecting all the columns")
        index_of_cols = []
        col_index=0
        for col in cols:
            col_index = 0
            for item in columns:
                if col == item:
                    test_index = col_index
                    # print("Index: " + str(test_index))
                    index_of_cols.append(test_index+1)
                col_index+=1

        testing = index_of_cols[:]

        for g in range(1,num_rows):
            # need some way to grab indexes of selected columns
            # index_of_cols = [g*num_cols+1,g*num_cols+2]
            # print(testing)
            for x in range(0,len(index_of_cols)):
                testing[x]= g*num_cols+index_of_cols[x]

            test = np.take(table,testing)
            print(test)
    elif cols[0]=="*":
        # select all the columns
        greg = True
        print(cols)
        print("Selecting all columns")
        index_of_cols = []
        for x in range(1,num_cols):
            index_of_cols.append(x)

        testing = index_of_cols[:]

        for g in range(1,num_rows):
            for x in range(0,len(index_of_cols)):
                testing[x]= g*num_cols+index_of_cols[x]

            test = np.take(table,testing)
            print(test)

def eval_create_table(table_name,cols):
    m=20 # number of rows
    index=0
    num_cols = len(cols)+1
    table = np.chararray((m,num_cols),itemsize=10)
    table.fill(0)
    np.put(table, index, table_name)
    for x in range(0,num_cols-1):
        np.put(table, x+1,cols[x])

    # loop to populate columns of our test db
    for i in range(1,m):
        table = create_test_db(table,index,num_cols,i)
        index += num_cols
    # print(table)
    columns = get_columns(table,num_cols)

    return table, num_cols, m

def create_test_db(table,index,num_cols,row_num):
    np.put(table, row_num*num_cols, row_num)
    np.put(table, row_num*num_cols+1,"John")
    np.put(table, row_num*num_cols+2,"Smith")
    np.put(table, row_num*num_cols+3,"3700 O St. NW")


    return table

def get_columns(table,num_cols):
    index_of_cols = []
    for x in range(1,num_cols):
        index_of_cols.append(x)
    columns = np.take(table,index_of_cols)
    return columns


def eval_delete(table_name, conditions):
    # TODO:
    #Find the table with table name
    #Find the tuple(s) with the relevant Conditions (using an index if it exists)
    #Remove those tuple(s) from the table
    return True

def eval_create_index(index_name, col_list):

    return True

def eval_drop_table(table_name):

    return True

def eval_drop_index(index_name, table_ref):

    return True

# eval_select(("first","last"),"customers",("x","=","1"))
# eval_create_table("customers",("first","last","address","phone"))
