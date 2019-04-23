# evaluator functions
# helpers
from __future__ import print_function
import numpy as np
from table import *
from database import *



def eval_select(database, cols, tables, conditions):
    # database,table,num_cols,num_rows = eval_create_table(database,"customers",("first","last","address"))
    # columns = database.relationList.index(tables).getColNames()
    if len(tables) == 1:
        if database.tableExists(tables[0]):
            table = database.getRelation(tables[0])
        else:
            print("Table does not exist.")
            return 0
    else:
        # join
        # table = database.getRelation("CUSTOMERS")
        print("there are multiple tables to select from")
    table = database.getRelation(tables[0])
    columns = table.getColNames()
    # print(table.relation)

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
        if not conditions:
            simple_select(table,table.numRows,table.numCols,index_of_cols,testing)
        elif conditions:
            num_conditions = (len(conditions)+1)/2
            if num_conditions == 1:
                simple_where(table,columns,conditions,table.numCols,table.numRows,index_of_cols)
            else:
                complex_where(table,columns,conditions,table.numCols,table.numRows,index_of_cols,num_conditions)

    elif cols[0]=="*":
        # select all the columns
        index_of_cols = []
        for x in range(1,table.numCols):
            index_of_cols.append(x)
        testing = index_of_cols[:]
        if not conditions:
            # handles simple select statement with no conditions
            simple_select(table,table.numRows,table.numCols,index_of_cols,testing)
        elif conditions:
            # handles a complex select statement
            num_conditions = (len(conditions)+1)/2
            if num_conditions == 1:
                simple_where(table,columns,conditions,table.numCols,table.numRows,index_of_cols)
            else:
                complex_where(table,columns,conditions,table.numCols,table.numRows,index_of_cols,num_conditions)

def complex_where(table,columns,conditions,num_cols,num_rows,index_of_cols,num_conditions):
    col_index = 0
    condition_num = 0
    matched_rows_list = []
    intersection_list = []
    union_list = []
    result = []
    itr = 1
    for l in range(0,num_conditions):
        col_index = 0
        the_column = conditions[condition_num][0]
        the_value = conditions[condition_num][2]

        for item in columns:
            if the_column == item:
                break
            else:
                col_index+=1
        list_of_vals = []
        row_nums_matched = []
        if conditions[condition_num][1] == "=":
            for x in range(1,num_rows):
                # print(np.take(table,x*num_cols+col_index+1))
                list_of_vals.append((x,np.take(table.relation,x*num_cols+col_index+1)))
            # print(list_of_vals)
            for val in range(0,len(list_of_vals)):
                if list_of_vals[val][1] == the_value:
                    row_nums_matched.append(list_of_vals[val][0])
            # print(row_nums_matched)
            matched_rows_list.append(row_nums_matched)
            # print(matched_rows_list)
            if len(matched_rows_list) > 1:
                if conditions[condition_num-1] == "and":
                    print("itr = " + (str(itr)))
                    intersection_list = list(set(matched_rows_list[0]) & set(matched_rows_list[itr]))
                    matched_rows_list[0] = intersection_list[:]
                    # print(intersection_list)
                    itr+=1
                elif conditions[condition_num-1] == "or":
                    intersection_list = list(set(matched_rows_list[0]) | set(matched_rows_list[itr]))
                    matched_rows_list[0] = intersection_list[:]
                    # print(intersection_list)
                    itr +=1
                # print(intersection_list)
            testing = index_of_cols[:]
            if l == num_conditions-1:
                if not intersection_list:
                    print("The query did not return any results")
                else:
                    for g in intersection_list:
                        for x in range(0,len(index_of_cols)):
                            testing[x]= g*num_cols+index_of_cols[x]
                        test = np.take(table.relation,testing)
                        print_output(test)
        elif conditions[condition_num][1] == "!=":
            # print("in the correct if else")
            for x in range(1,num_rows):
                list_of_vals.append((x,np.take(table.relation,x*num_cols+col_index+1)))
            for val in range(0,len(list_of_vals)):
                if list_of_vals[val][1] != the_value:
                    row_nums_matched.append(list_of_vals[val][0])
            matched_rows_list.append(row_nums_matched)
            # print(matched_rows_list)
            if len(matched_rows_list) > 1:
                if conditions[condition_num-1] == "and":
                    intersection_list = list(set(matched_rows_list[0]) & set(matched_rows_list[itr]))
                    matched_rows_list[0] = intersection_list[:]
                    # print(intersection_list)
                    itr += 1
                elif conditions[condition_num-1] == "or":
                    intersection_list = list(set(matched_rows_list[0]) | set(matched_rows_list[itr]))
                    matched_rows_list[0] = intersection_list[:]
                    # print(intersection_list)
                    itr +=1
            testing = index_of_cols[:]
            if l == num_conditions-1:
                if not intersection_list:
                    print("The query did not return any results")
                else:
                    for g in intersection_list:
                        for x in range(0,len(index_of_cols)):
                            testing[x]= g*num_cols+index_of_cols[x]
                        # result.append(np.take(table,testing))
                        test = np.take(table.relation,testing)
                        print_output(test)
        condition_num += 2

def simple_where(table,columns,conditions,num_cols,num_rows,index_of_cols):
    col_index = 0
    first_col = conditions[0][0]
    first_val = conditions[0][2]
    for item in columns:
        if first_col == item:
            # print(col_index)
            break
        else:
            col_index+=1
    list_of_vals = []
    row_nums_matched = []
    if conditions[0][1] == "=":
        for x in range(1,num_rows):
            list_of_vals.append((x,np.take(table.relation,x*num_cols+col_index+1)))
        # print(list_of_vals)
        for val in range(0,len(list_of_vals)):
            if list_of_vals[val][1] == first_val:
                row_nums_matched.append(list_of_vals[val][0])
        if not row_nums_matched:
            print("The query did not return any results")
        else:
            # print(row_nums_matched)
            result = []
            testing = index_of_cols[:]
            for g in row_nums_matched:
                for x in range(0,len(index_of_cols)):
                    testing[x]= g*num_cols+index_of_cols[x]
                test = np.take(table.relation,testing)
                print_output(test)
    elif conditions[0][1] == "!=":
        for x in range(1,num_rows):
            list_of_vals.append((x,np.take(table.relation,x*num_cols+col_index+1)))
        # print(list_of_vals)
        for val in range(0,len(list_of_vals)):
            if list_of_vals[val][1] != first_val:
                row_nums_matched.append(list_of_vals[val][0])
        if not row_nums_matched:
            print("The query did not return any results")
        else:
            # print(row_nums_matched)
            result = []
            # must select indices of cols for each row in row_nums_matched
            testing = index_of_cols[:]
            for g in row_nums_matched:
                for x in range(0,len(index_of_cols)):
                    testing[x]= g*num_cols+index_of_cols[x]

                test = np.take(table.relation,testing)
                print_output(test)

# handles a simple select statement without conditions
def simple_select(table,num_rows,num_cols,index_of_cols,testing):
    for g in range(1,num_rows):
        for x in range(0,len(index_of_cols)):
            testing[x]= g*num_cols+index_of_cols[x]
        # print(testing)
        test = np.take(table.relation,testing)
        print_output(test)

def print_output(result):
    output_list = []
    for x in range(0,len(result)):
        output_list.append(result[x])
    print("| ", end="")
    for item in output_list:
        print('{0: <10}'.format(item), end= " | ")
        # print("|  "+item,end='\t')
    print("")
    # print("------------------------------")

def save_state(table):
    file = "outfile"
    table.tofile(file,sep=",",format="%s")
    # np.save(file,table)

def restore_state():
    file = "outfile"
    # table.fromfile(file,sep=",",format="%s")
    # table = np.load(file)
    # this isn't working but simple writing to text file is just as easy
    # could also just store commands in text file and rerun them

    # return table

def eval_insert(database,table_name,values):
    # database,table,num_cols,num_rows = eval_create_table(database,"customers",("first","last","address"))
    # columns = get_columns(table,num_cols)
    print(values)
    table = database.getRelation(table_name)
    columns = table.getColNames()
    num_rows = table.numRows
    num_cols = table.numCols
    cols = []
    index_of_cols = []
    vals = []
    row_num = 1 # if we want it sorted, just figure out a way to set row_num
    # test_values = [("first","last","address"),"values",("adam","jones","arizona")]
    for col in values[0]:
        cols.append(col)
    for val in values[2]:
        vals.append(val)
    for col in cols:
        col_index = 0
        for item in columns:
            if col == item:
                test_index = col_index
                index_of_cols.append(test_index+1)
            col_index+=1

    table.relation.resize((num_rows+1,num_cols))
    table.setNumRows(num_rows+1)
    row_num = num_rows
    np.put(table.relation,row_num*num_cols,row_num)
    for x in range(0,len(vals)):
        np.put(table.relation,row_num*num_cols+index_of_cols[x],vals[x])
    print(table)
    return table

def eval_update(database,table_name,col_vals,conditions):
    table_name, col_vals, conditions = ("customers",[("first","=","hodor"),"and",("last","=","testing123")],[("last","=","wills"),"or",("last","!=","doe")])
    print(col_vals)
    print(conditions)
    # database,table,num_cols,num_rows = eval_create_table(database,"customers",("first","last","address"))
    # columns = get_columns(table,num_cols)
    table = database.getRelation(table_name)
    columns = table.getColNames()
    num_conditions = (len(conditions)+1)/2
    index_of_col_conditions = 0
    index_of_col_value = 0
    col_index = 0
    cols = []
    vals = []
    search_cols = []
    search_vals = []
    index_of_cols1 = []
    index_of_cols2 = []
    list_of_vals = []
    matched_rows_list = []
    row_nums_matched = []

    for item in col_vals:
        if item != "and" and item != "or":
            cols.append(item[0])
            vals.append(item[2])
    for item in conditions:
        if item != "and" and item != "or":
            search_cols.append(item[0])
            search_vals.append(item[2])
    # find index of columns to replace
    for col in cols:
        col_index = 0
        for item in columns:
            if col == item:
                test_index = col_index
                index_of_cols1.append(test_index+1)
            col_index+=1
    # find index of column to search for value
    for col in search_cols:
        col_index = 0
        for item in columns:
            if col == item:
                test_index = col_index
                index_of_cols2.append(test_index+1)
            col_index+=1

    itr = 0
    val_num = 0
    condition_num = 0
    intersection_list = []
    for l in range(0,num_conditions):
        for x in range(1,num_rows):
            list_of_vals.append((x,np.take(table.relation,x*num_cols+index_of_cols2[l]))) # TODO: index error here
        for val in range(0,len(list_of_vals)):
            if conditions[condition_num][1] == "=":
                if list_of_vals[val][1] == search_vals[l]:
                    row_nums_matched.append(list_of_vals[val][0])
            elif conditions[condition_num][1] == "!=":
                if list_of_vals[val][1] != search_vals[l]:
                    row_nums_matched.append(list_of_vals[val][0])
            #print(row_nums_matched)
        matched_rows_list.append(row_nums_matched)
        if len(matched_rows_list) > 1:
            if conditions[condition_num-1] == "and":
                print("itr = " + (str(itr)))
                intersection_list = list(set(matched_rows_list[0]) & set(matched_rows_list[itr]))
                matched_rows_list[0] = intersection_list[:]
                # print(intersection_list)
                itr+=1
            elif conditions[condition_num-1] == "or":
                intersection_list = list(set(matched_rows_list[0]) | set(matched_rows_list[itr]))
                matched_rows_list[0] = intersection_list[:]
                itr +=1
        # print("intersection list : " + str(intersection_list))
        testing = index_of_cols1[:]
        if l == num_conditions-1:
            if not intersection_list:
                print("The query did not return any results")
            else:
                # print(intersection_list)
                for g in intersection_list:
                    for x in range(0,len(index_of_cols1)):
                        testing[x]= g*num_cols+index_of_cols1[x]
                        np.put(table.relation,g*num_cols+index_of_cols1[x],vals[x])

        condition_num+=2

    print(table)
    return database

def eval_create_table(database,table_name,cols):
    m=1 # number of rows
    index=0
    num_cols = len(cols)+1
    # dtype = np.dtype([('key', int), ('first', 'S10'), ('last', 'S10'), ('address','S10')])
    # table = np.chararray((m,num_cols),itemsize=20)
    table = Table(m,num_cols)
    table.setName(table_name)
    table.setNumCols(num_cols)
    table.setNumRows(m)
    table.relation.fill(0)
    np.put(table.relation, index, "key")
    for x in range(1,table.numCols):
        np.put(table.relation, x,cols[x-1])
    database.addRelation(table)
    print(table.relation)

    # print(str(table_name) + " successfully created")

    return database

def create_test_db(table,index,num_cols,row_num):
    np.put(table.relation, row_num*num_cols, row_num)
    np.put(table.relation, row_num*num_cols+1,"john")
    np.put(table.relation, row_num*num_cols+2,"smith")
    np.put(table.relation, row_num*num_cols+3,"3700 O St. NW")

    return table

# return a list of column names in the given relation
def get_columns(table,num_cols):
    index_of_cols = []
    for x in range(1,num_cols):
        index_of_cols.append(x)
    columns = np.take(table.relation,index_of_cols)
    return columns

def eval_delete(database,table_name, conditions):
    tempTable = Table(10,10) # TODO: Grab the correct table using the table_name
    #Find the tuple(s) with the relevant Conditions (using an index if it exists)
    #if table[len(table)-1] != -1: #There is an index TODO: Handle index
        #
    #else:
    database,table,num_cols,num_rows = eval_create_table(database,"customers",("first","last","address"))
    columns = get_columns(table,num_cols)

    cols = []
    vals = []
    deleted_rows = []
    index_of_cols = []
    list_of_vals = []
    for item in conditions:
        # print(item)
        if item != "and" and item != "or":
            cols.append(item[0])
            vals.append(item[2])

    for col in cols:
        col_index = 0
        for item in columns:
            if col == item:
                test_index = col_index
                index_of_cols.append(test_index+1)
            col_index+=1

    for val in vals:
        for x in range(1,num_rows):
            # print("Test: " + str(np.take(table,index_of_col*num_cols*x)))
            # print("Test: "+ str(np.take(table,num_cols*x+index_of_cols2[itr])))
            if val == np.take(table.relation,num_cols*x+index_of_cols[itr]):
                itr+=1
                break

    for tuple in conditions:
        col_name = tuple[0]
        print(tuple)



    #Remove those tuple(s) from the table
    return True

def test_sort(table):
    table.sort(axis=0)
    print(table)
    print("this is just a test, the table structure has not changed")

def eval_create_index(database,index_name, table_name, col_list):
    # NOTE: These are done using the new Table class
    tempTable = Table(10,10) # TODO: Grab the correct table using the table_name

    for tuple in col_list:
        col_name = tuple[0]
        ordering = tuple[1]
        tempTable.addIndex(index_name, col_name, ordering)

    return tempTable

def eval_drop_table(database,table_name):
    table_exists = False
    if database.tableExists(table_name):
        for relation in database.relationList:
            if relation.name == table_name.upper():
                database.relationList.remove(relation)
        print(table_name.upper() + " successfully deleted.")
        return database
    else:
        print("Could not find relation with the name " + str(table_name.upper()))
        return database

def eval_drop_index(database,index_name, table_ref):

    tempTable = Table(10,10) # TODO: grab the correct table using table_ref

    for tuple in tempTable.indicies:
        if tuple[0] == index_name:
            tempTable.indices.remove(tuple)

    return tempTable

def merge_scan(table1, table2, joining_attr):
    # Sort each table on the joining attr
    # Match the rows based on the joining attr
    # Create one large table with all the new rows
    return 0

# def print_relation(table):
#     index_list = []
#     for x in range(0,table.numRows):
#         index_list.extend(range(x*table.numCols, table.numCols*))
#         row = np.take(table.relation,index_list)
#         print_output(row)

def load_relations():
    # this works alright but waiting to talk with you about exactly what he wants
    database = Database()
    # this might be what we're looking for - 5 rows and cols for visibility
    test = Table(5,5)
    test.setName("test")
    for row in range(0,test.numRows):
        for col in range(0,test.numCols):
            np.put(test.relation,row*test.numCols+col,row)
    database.addRelation(test)
    print(test.relation)

    #*** Relation 1
    r1 = Table(100,100)
    r1.setName("Relation1")
    for row in range(0,r1.numRows):
        for col in range(0,r1.numCols):
            np.put(r1.relation,row*r1.numCols+col,(col+1)*(row+1))
    database.addRelation(r1)
    # print(r1.relation)

    #*** Relation 2
    r2 = Table(20,20)
    r2.setName("Relation2")
    for row in range(0,r2.numRows):
        for col in range(0,r2.numCols):
            np.put(r2.relation,row*r2.numCols+col,(col+1)*(row+1))
    database.addRelation(r2)
    # print(r2.relation)
    # print_relation(r2)

    #*** Relation 3
    r3 = Table(40,40)
    r3.setName("Relation3")
    r3.relation.fill(1)
    for i in range(0,r3.numCols):
        np.put(r3.relation, i*r3.numCols, i)
    np.put(r3.relation,0,1)
    database.addRelation(r3)
    # print(r3.relation)

    #*** loads test relation
    index=0
    num_cols=3
    m=20
    cols = ["first","last","address"]
    table = Table(m,num_cols+1)
    table.setName("customers")
    table.relation.fill(0)
    np.put(table.relation, index, "key")

    for x in range(0,num_cols):
        np.put(table.relation, x+1,cols[x])

    # loop to populate columns of our test db
    for i in range(1,m):
        table = create_test_db(table,index,num_cols+1,i)
        index += num_cols
    # print(table)
    columns = get_columns(table,num_cols)
    np.put(table.relation,29,"jane")
    np.put(table.relation,30,"doe")
    np.put(table.relation,33,"greg")
    np.put(table.relation,34,"wills")
    np.put(table.relation,37,"donald")
    np.put(table.relation,38,"trump")
    print(table.relation)
    print("\n")

    database.addRelation(table)
    for relation in database.relationList:
        print(relation.name)

    return database

# eval_select(("first","last"),"customers",[("first","=","John"),("last","=","smith")])
# eval_create_table("customers",("first","last","address"))
# table = eval_insert("customers",[("first","last"),"values",("adam","jones","arizona")])
# table = eval_update("customers",("first","=","hodor"),("last","=","doe"))
# eval_delete("customers",[("first","=","john")])
# database = load_relations()
