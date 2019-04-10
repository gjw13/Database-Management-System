# evaluator functions
# helpers
from __future__ import print_function
import numpy as np


def eval_select(cols, tables, conditions):
    table,num_cols,num_rows = eval_create_table("customers",("first","last","address"))
    columns = get_columns(table,num_cols)
    if cols[0] != "*":
        index_of_cols = []
        col_index=0
        # nested for loop gets indexes of columns selected in variable cols
        for col in cols:
            col_index = 0
            for item in columns:
                if col == item:
                    test_index = col_index
                    index_of_cols.append(test_index+1)
                col_index+=1

        testing = index_of_cols[:]
        # print("-------------------------")
        if not conditions:
            simple_select(table,num_rows,num_cols,index_of_cols,testing)
        elif conditions:
            col_index = 0
            # only works for the first condition so far
            first_col = conditions[0][0]
            first_val = conditions[0][2]
            for item in columns:
                if first_col == item:
                    print(col_index)
                    break
                else:
                    col_index+=1
            list_of_vals = []
            row_nums_matched = []
            if conditions[0][1] == "=":
                for x in range(1,num_rows):
                    list_of_vals.append((x,np.take(table,x*num_cols+col_index+1)))
                print(list_of_vals)
                for val in range(0,len(list_of_vals)):
                    if list_of_vals[val][1] == first_val:
                        row_nums_matched.append(list_of_vals[val][0])
                if not row_nums_matched:
                    print("The query did not return any results")
                else:
                    print(row_nums_matched)
                    result = []
                    # must select indices of cols for each row in row_nums_matched
                    testing = index_of_cols[:]

                    for g in row_nums_matched:
                        for x in range(0,len(index_of_cols)):
                            testing[x]= g*num_cols+index_of_cols[x]

                        test = np.take(table,testing)
                        print_output(test)

            elif conditions[0][1] == "!=":
                for x in range(1,num_rows):
                    list_of_vals.append((x,np.take(table,x*num_cols+col_index+1)))
                print(list_of_vals)
                for val in range(0,len(list_of_vals)):
                    if list_of_vals[val][1] != first_val:
                        row_nums_matched.append(list_of_vals[val][0])
                if not row_nums_matched:
                    print("The query did not return any results")
                else:
                    print(row_nums_matched)
                    result = []
                    # must select indices of cols for each row in row_nums_matched
                    testing = index_of_cols[:]
                    for g in row_nums_matched:
                        for x in range(0,len(index_of_cols)):
                            testing[x]= g*num_cols+index_of_cols[x]

                        test = np.take(table,testing)
                        print_output(test)
    elif cols[0]=="*":
        # select all the columns
        index_of_cols = []
        for x in range(1,num_cols):
            index_of_cols.append(x)
        testing = index_of_cols[:]
        if not conditions:
            # handles simple select statement with no conditions
            simple_select(table,num_rows,num_cols,index_of_cols,testing)
        elif conditions:
            # handles a complex select statement
            col_index = 0
            # only works for the first condition so far
            first_col = conditions[0][0]
            first_val = conditions[0][2]
            # finds index of column given in condition
            for item in columns:
                if first_col == item:
                    print(col_index)
                    break
                else:
                    col_index+=1
            list_of_vals = []
            row_nums_matched = []
            if conditions[0][1] == "=":
                for x in range(1,num_rows):
                    list_of_vals.append((x,np.take(table,x*num_cols+col_index+1)))
                print(list_of_vals)
                for val in range(0,len(list_of_vals)):
                    if list_of_vals[val][1] == first_val:
                        row_nums_matched.append(list_of_vals[val][0])
                if not row_nums_matched:
                    print("The query did not return any results")
                else:
                    print(row_nums_matched)
                    result = []
                    # must select indices of cols for each row in row_nums_matched
                    testing = index_of_cols[:]

                    for g in row_nums_matched:
                        for x in range(0,len(index_of_cols)):
                            testing[x]= g*num_cols+index_of_cols[x]

                        test = np.take(table,testing)
                        print_output(test)

            elif conditions[0][1] == "!=":
                for x in range(1,num_rows):
                    list_of_vals.append((x,np.take(table,x*num_cols+col_index+1)))
                print(list_of_vals)
                for val in range(0,len(list_of_vals)):
                    if list_of_vals[val][1] != first_val:
                        row_nums_matched.append(list_of_vals[val][0])
                if not row_nums_matched:
                    print("The query did not return any results")
                else:
                    print(row_nums_matched)
                    result = []
                    # must select indices of cols for each row in row_nums_matched
                    testing = index_of_cols[:]
                    for g in row_nums_matched:
                        for x in range(0,len(index_of_cols)):
                            testing[x]= g*num_cols+index_of_cols[x]

                        test = np.take(table,testing)
                        print_output(test)
            # row_nums_matched contains list that holds the rows that match condition
    save_state(table)
    new_table = restore_state()
    print(new_table)

# handles a simple select statement without conditions
def simple_select(table,num_rows,num_cols,index_of_cols,testing):
    for g in range(1,num_rows):
        for x in range(0,len(index_of_cols)):
            testing[x]= g*num_cols+index_of_cols[x]
        test = np.take(table,testing)
        print_output(test)

def print_output(result):
    output_list = []
    for x in range(0,len(result)):
        output_list.append(result[x])
    for item in output_list:
        print("|  "+item,end='\t')
    print("|")

def save_state(table):
    file = "outfile"
    table.tofile(file,sep=",",format="%s")
    # np.save(file,table)

def restore_state():
    file = "outfile"
    # table = fromfile(file,sep=",",format="%s")
    # table = np.load(file)
    # this isn't working but simple writing to text file is just as easy
    # could also just store commands in text file and rerun them

    # return table

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
    np.put(table,29,"jane")
    np.put(table,30,"doe")
    print(table)

    return table, num_cols, m

def create_test_db(table,index,num_cols,row_num):
    np.put(table, row_num*num_cols, row_num)
    np.put(table, row_num*num_cols+1,"john")
    np.put(table, row_num*num_cols+2,"smith")
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

eval_select(("first","last"),"customers",[("first","=","John"),("last","=","smith")])
# eval_create_table("customers",("first","last","address","phone"))
