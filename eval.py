# evaluator functions
# helpers
from __future__ import print_function
import numpy as np
from table import *
from database import *
import pickle
import os
from os import listdir
from os.path import isfile, join
import copy
from collections import OrderedDict



def eval_select(database, cols, tables, conditions):
    # database,table,num_cols,num_rows = eval_create_table(database,"customers",("first","last","address"))
    # columns = database.relationList.index(tables).getColNames()

    # If there's an index on one of the conditions:
    #   Create a new table by selecting all the rows with just the index condition
    #   If that's the only condition, return the table
    #   Otherwise send the new table back to eval_select
    result_list = []
    index_marker = False
    other_conditions = []
    for table in tables:
        if type(table) is tuple:
            table_name = table[0]
        else:
            table_name = table
        if database.tableExists(table_name):
            table_obj = database.getRelation(table_name)
            if len(table_obj.getIndicies()) > 0:
                for index in table_obj.getIndicies():
                    for condition in conditions:
                        # Check condition against index col_name
                        if len(conditions) == 1 and index[1] == condition[0]:
                            # Proceed with the select as normal
                            break
                        elif index[1] == condition[0]:
                            index_marker = True
                            for condition2 in conditions:
                                if condition2 is not condition:
                                    other_conditions.append(condition2)
        else:
            print("Relation \'" + table_name.upper() + "\' does not exist.")
            return 0
    # commented this out cuz could some problems with two relations
    # for col in cols:
    #     if col not in table_obj.getColNames():
    #         print("One or more of your columns does not exist.")
    #         return 0

    if len(tables) == 1:
        if database.tableExists(tables[0]):
            table = database.getRelation(tables[0])
        else:
            print("Table does not exist.")
            return 0
    else:
        # Get the joining attrs from the where clause
        dot_index = -1
        for tuple_t in conditions:
            if "." in tuple_t[0]:
                dot_index = conditions.index(tuple_t)
        joining_cond = conditions[dot_index]
        conditions.remove(joining_cond)
        #print(joining_cond)

        # join
        i = 0
        table = Table(1,1)
        while i < len(tables)-1: # ASSUMPTION: Tables have aliases
            t1_name = tables[i][0]
            t1_alias = tables[i][1]
            join_index = [j for j, s in enumerate(joining_cond) if t1_alias+"." in s]
            temp_attr = joining_cond[join_index[0]]
            t1_join_attr_temp = temp_attr.replace(".", "")
            t1_join_attr = t1_join_attr_temp.replace(t1_alias, "", 1)
            #print(t1_join_attr)

            t2_name = tables[i+1][0]
            t2_alias = tables[i+1][1]
            #print(t2_alias)
            join_index = [k for k, s in enumerate(joining_cond) if t2_alias+"." in s]
            #print(join_index)
            temp_attr = joining_cond[join_index[0]]
            t2_join_attr_temp = temp_attr.replace(".", "")
            t2_join_attr = t2_join_attr_temp.replace(t2_alias, "", 1)
            #print(t2_join_attr)

            table = merge_scan(database.getRelation(t1_name), database.getRelation(t2_name), t1_join_attr, t2_join_attr)
            #print(table.relation)
            i+=1
        # table = database.getRelation("CUSTOMERS")
        #print("there are multiple tables to select from")
    #table = database.getRelation(tables[0])
    columns = table.getColNames()
    for cond in conditions:
        if cond != "and" and cond != "or":
            if not table.columnExists(cond[0]):
                print("Column name \'" + str(cond[0]) + "\' did not match existing column in relation. ")
                return 0
    if cols[0] != "*":
        index_of_cols = []
        col_index=0
        # nested for loop gets indexes of columns selected in variable cols
        for col in cols:
            col_index = 0
            for item in columns:
                if col == item:
                    test_index = col_index
                    index_of_cols.append(test_index)
                col_index+=1
        testing = index_of_cols[:]
        if not conditions:
            result_list = simple_select(table,table.numRows,table.numCols,index_of_cols,testing)
        elif conditions:
            num_conditions = (len(conditions)+1)/2
            if num_conditions == 1:
                result_list = simple_where(table,columns,conditions,table.numCols,table.numRows,index_of_cols)
            else:
                result_list = complex_where(table,columns,conditions,table.numCols,table.numRows,index_of_cols,num_conditions)

    elif cols[0]=="*":
        # select all the columns
        index_of_cols = []
        for x in range(0,table.numCols):
            index_of_cols.append(x)
        testing = index_of_cols[:]
        if not conditions:
            # handles simple select statement with no conditions
            result_list = simple_select(table,table.numRows,table.numCols,index_of_cols,testing)
        elif conditions:
            # handles a complex select statement
            num_conditions = (len(conditions)+1)/2
            if num_conditions == 1:
                result_list = simple_where(table,columns,conditions,table.numCols,table.numRows,index_of_cols)
            else:
                result_list = complex_where(table,columns,conditions,table.numCols,table.numRows,index_of_cols,num_conditions)



    # Handle result_list into table object for return
    result_table = Table(len(result_list), len(result_list[0]))
    result_table.setName("temptable")
    i = 0
    indicies = []
    while i < len(result_list[0]):
        indicies.append(i)
        i+=1
    j = 0
    for char_array in result_list:
        i = 0
        temp_arr = np.take(char_array, indicies)
        while i < len(temp_arr):
            np.put(result_table.relation, j, temp_arr[i])
            i+=1
            j+=1


    # Re-do the eval_select
    if index_marker:
        database.addRelation(result_table)
        print("\n\nFinal Output:\n")
        eval_select(database, cols, "temptable", other_conditions)
        databse.removeRelation(result_table)


def complex_where(table,columns,conditions,num_cols,num_rows,index_of_cols,num_conditions):
    # print("complex where)")
    #print(index_of_cols)
    col_index = 0
    condition_num = 0
    matched_rows_list = []
    intersection_list = []
    union_list = []
    result_list = []
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
        for x in range(1,num_rows):
            # print(np.take(table,x*num_cols+col_index+1))
            list_of_vals.append((x,np.take(table.relation,x*num_cols+col_index)))
        # print(list_of_vals)
        for val in range(0,len(list_of_vals)):
            if conditions[condition_num][1] == "=":
                if list_of_vals[val][1] == the_value:
                    row_nums_matched.append(list_of_vals[val][0])
            elif conditions[condition_num][1] == "!=":
                if list_of_vals[val][1] != the_value:
                    row_nums_matched.append(list_of_vals[val][0])
            elif conditions[condition_num][1] == "<":
                if int(list_of_vals[val][1]) < int(the_value):
                    row_nums_matched.append(list_of_vals[val][0])
            elif conditions[condition_num][1] == ">":
                if int(list_of_vals[val][1]) > int(the_value):
                    row_nums_matched.append(list_of_vals[val][0])
            elif conditions[condition_num][1] == "<=":
                if int(list_of_vals[val][1]) <= int(the_value):
                    row_nums_matched.append(list_of_vals[val][0])
            elif conditions[condition_num][1] == ">=":
                if int(list_of_vals[val][1]) >= int(the_value):
                    row_nums_matched.append(list_of_vals[val][0])
        #print(row_nums_matched)
        matched_rows_list.append(row_nums_matched)
        # print(matched_rows_list)
        if len(matched_rows_list) > 1:
            if conditions[condition_num-1] == "and":
                # print("itr = " + (str(itr)))
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
                return []
            else:
                i=1
                attrIndexes = []
                attrIndexes.extend(range(0,num_cols))
                temp = np.take(table.relation,index_of_cols)
                #print_output(temp)
                for g in intersection_list:
                    for x in range(0,len(index_of_cols)):
                        testing[x]= g*num_cols+index_of_cols[x]
                    test = np.take(table.relation,testing)
                    result_list.append(test)
                    if i == 1:
                        s = ""
                        print(s.ljust(len(index_of_cols)*13+1, "-"))
                        i+=1
                    print_output(test)
        condition_num += 2
    return result_list

def simple_where(table,columns,conditions,num_cols,num_rows,index_of_cols):
    # print("simple where")
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

    for x in range(1,num_rows):
        list_of_vals.append((x,np.take(table.relation,x*num_cols+col_index)))
    # print(list_of_vals)
    for val in range(0,len(list_of_vals)):
        if conditions[0][1] == "=":
            if list_of_vals[val][1] == first_val:
                row_nums_matched.append(list_of_vals[val][0])
        elif conditions[0][1] == "!=":
            if list_of_vals[val][1] != first_val:
                row_nums_matched.append(list_of_vals[val][0])
        elif conditions[0][1] == "<":
            if int(list_of_vals[val][1]) < int(first_val):
                row_nums_matched.append(list_of_vals[val][0])
        elif conditions[0][1] == ">":
            if int(list_of_vals[val][1]) > int(first_val):
                row_nums_matched.append(list_of_vals[val][0])
        elif conditions[0][1] == ">=":
            if int(list_of_vals[val][1]) >= int(first_val):
                row_nums_matched.append(list_of_vals[val][0])
        elif conditions[0][1] == "<=":
            if int(list_of_vals[val][1]) <= int(first_val):
                row_nums_matched.append(list_of_vals[val][0])
    if not row_nums_matched:
        print("The query did not return any results")
        return []
    else:
        # print(row_nums_matched)
        result = []
        testing = index_of_cols[:]
        temp = np.take(table.relation,index_of_cols)
        #print_output(temp)
        s = ""
        print(s.ljust(len(index_of_cols)*13+1, "-"))
        for g in row_nums_matched:
            for x in range(0,len(index_of_cols)):
                testing[x]= g*num_cols+index_of_cols[x]
            test = np.take(table.relation,testing)
            result.append(test)
            print_output(test)
        return result

# handles a simple select statement without conditions
def simple_select(table,num_rows,num_cols,index_of_cols,testing):
    result_list = []
    for g in range(0,num_rows):
        for x in range(0,len(index_of_cols)):
            testing[x]= g*num_cols+index_of_cols[x]
        # print(testing)
        test = np.take(table.relation,testing)
        result_list.append(test)
        print_output(test)
        if g == 0:
            s = ""
            print(s.ljust(len(index_of_cols)*13+1, "-"))
    return result_list

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

def save_state(database):
    # file = "outfile"
    dir = "Storage"
    # database.getRelation("CUSTOMERS").relation.tofile(file,sep="")
    for relation in database.relationList:
        filename = str(relation.name)
        cwd = os.getcwd()
        file = os.path.join(cwd,dir,filename)
        with open(file, 'wb') as output:
            pickle.dump(relation, output, pickle.HIGHEST_PROTOCOL)
        # relation.relation.dump(file)

def restore_state():
    database = Database()
    relationList = []
    dir = "Storage"
    # table = np.load(file)
    cwd = os.getcwd()
    mypath = os.path.join(cwd,dir)
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    # print(onlyfiles)
    for file in onlyfiles:
        file = os.path.join(mypath,file)
        with open(file, 'rb') as input:
            relation = pickle.load(input)
            database.relationList.append(relation)
    return database

# TODO: Check if all the values are the same as another tuple
def eval_insert(database,table_name,values):
    # database,table,num_cols,num_rows = eval_create_table(database,"customers",("first","last","address"))
    # columns = get_columns(table,num_cols)
    #print(values)
    table = database.getRelation(table_name)
    columns = table.getColNames()
    num_rows = table.numRows
    num_cols = table.numCols
    index_of_cols = []
    i = 0
    while i < num_cols:
        index_of_cols.append(i)
        i+=1

    temp_list = table.relation.tolist()

    for tuple in temp_list:
        if values[0] == tuple[0]:
            print("Duplicate Tuple! Not allowed.")
            return database
        elif sorted(tuple) == sorted(values):
            print("Duplicate Tuple! Not allowed.")
            return database

    copy_table = copy.deepcopy(table)
    copy_table.relation.resize((num_rows+1,num_cols))
    table.setNumRows(num_rows+1)
    row_num = num_rows
    #np.put(table.relation,row_num*num_cols,row_num)
    for x in range(0,len(values)):
        np.put(copy_table.relation,row_num*num_cols+index_of_cols[x],values[x])
    table.relation = copy_table.relation
    print("Successful insert.")
    return database


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
    table.setColNames(cols)
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
    np.put(table.relation, row_num*num_cols+3,"22")

    return table

# return a list of column names in the given relation
def get_columns(table,num_cols):
    index_of_cols = []
    for x in range(1,num_cols):
        index_of_cols.append(x)
    columns = np.take(table.relation,index_of_cols)
    return columns

def eval_delete(database, table_name, conditions):
    table = database.getRelation(table_name)
    columns = table.getColNames()
    num_rows = table.numRows
    num_cols = table.numCols
    num_conditions = (len(conditions)+1)/2
    condition_num = 0
    col_index = 0
    index_of_cols = []
    matched_rows_list = []
    intersection_list = []
    union_list = []
    result_list = []
    replace_index_list = []
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
        for x in range(1,num_rows):
            # print(np.take(table,x*num_cols+col_index+1))
            list_of_vals.append((x,np.take(table.relation,x*num_cols+col_index)))
        # print(list_of_vals)
        for val in range(0,len(list_of_vals)):
            print(list_of_vals[val][1])
            print(the_value)
            if conditions[condition_num][1] == "=":
                if list_of_vals[val][1] == the_value:
                    row_nums_matched.append(list_of_vals[val][0])
            elif conditions[condition_num][1] == "!=":
                if list_of_vals[val][1] != the_value:
                    row_nums_matched.append(list_of_vals[val][0])
            elif conditions[condition_num][1] == "<":
                if int(list_of_vals[val][1]) < int(the_value):
                    row_nums_matched.append(list_of_vals[val][0])
            elif conditions[condition_num][1] == ">":
                if int(list_of_vals[val][1]) > int(the_value):
                    row_nums_matched.append(list_of_vals[val][0])
            elif conditions[condition_num][1] == "<=":
                if int(list_of_vals[val][1]) <= int(the_value):
                    row_nums_matched.append(list_of_vals[val][0])
            elif conditions[condition_num][1] == ">=":
                if int(list_of_vals[val][1]) >= int(the_value):
                    row_nums_matched.append(list_of_vals[val][0])
        print(row_nums_matched)
        matched_rows_list.append(row_nums_matched)
        print(matched_rows_list)
        if len(matched_rows_list) > 1:
            if conditions[condition_num-1] == "and":
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
        elif len(matched_rows_list) == 1:
            intersection_list = matched_rows_list[0]
        testing = index_of_cols[:]
        print(intersection_list)
        if l == num_conditions-1:
            if not intersection_list:
                print("The conditions given could not be found.")
                return []
            else:
                index=0
                for g in intersection_list:
                    replace_index_list = []
                    for a in range(1,table.numCols):
                        replace_index_list.append(int(num_cols*g+a))
                    print(replace_index_list)
                    start_index = table.numRows*table.numCols-num_cols
                    index_list = []
                    index_list.extend(range(start_index+1-index,start_index+num_cols-index))
                    temp = np.take(table.relation,index_list) # temp contains the right (last) tuple
                    for x in range(0,len(temp)):
                        np.put(table.relation,replace_index_list[x],temp[x])
                    # test = np.take(table.relation,testing)
                    # result_list.append(test)
                    # print_output(test)
                    index+=num_cols
                table.relation = np.resize(table.relation,(num_rows-len(intersection_list),num_cols))
                table.setNumRows(num_rows-len(intersection_list))
                num_rows = num_rows-len(intersection_list)
                print(table.relation)
        condition_num += 2
    print(database)
    return database

def eval_create_index(database,index_name, table_name, col_list):
    if database.tableExists(table_name):
        table_obj = database.getRelation(table_name)
        for tuple in col_list:
            col_name = tuple[0]
            ordering = tuple[1]
            table_obj.addIndex(index_name, col_name, ordering)
            print("Index Created with name: " + index_name)


def eval_drop_table(database,table_name):
    dir = "Storage"
    cwd = os.getcwd()
    if database.tableExists(table_name):
        for relation in database.relationList:
            if relation.name == table_name.upper():
                database.relationList.remove(relation)
                file = os.path.join(cwd,dir,table_name.upper())
                if(os.path.isfile(file)):
                    os.remove(file)
        print(table_name.upper() + " successfully deleted.")
        return database
    else:
        print("Could not find relation with the name " + str(table_name.upper()))
        return database

def eval_drop_index(database,index_name, table_ref):
    if database.tableExists(table_ref):
        for relation in database.relationList:
            if relation.name == table_ref.upper():
                for tuple in relation.indices:
                    if tuple[0] == index_name:
                        relation.indices.remove(tuple)
                        print("Index succesfully deleted.")
                        return database
    print("Could not find index with name " + index_name)
    return database


def list_sort(list, index):
    list.sort(key = lambda x:x[0])
    return list


def merge_scan(table1, table2, joining_attr_t1, joining_attr_t2):

    # Check if the joining_attr is a number
    # Sort each table on the joining attr
    try:
        int_val = int(table1.relation[1,table1.colNames.index(joining_attr_t1)])
        temp_t1 = table1.relation.tolist()
        for line in temp_t1:
            if temp_t1.index(line) != 0:
                line[table1.colNames.index(joining_attr_t1)] = int(line[table1.colNames.index(joining_attr_t1)])
        temp_t2 = table2.relation.tolist()
        for line in temp_t2:
            if temp_t2.index(line) != 0:
                line[table2.colNames.index(joining_attr_t2)] = int(line[table2.colNames.index(joining_attr_t2)])
        sorted_t1 = list_sort(temp_t1, table1.colNames.index(joining_attr_t1))
        sorted_t2 = list_sort(temp_t2, table2.colNames.index(joining_attr_t2))
    except:
        sorted_t1 = list_sort(table1.relation.tolist(), table1.colNames.index(joining_attr_t1))
        sorted_t2 = list_sort(table2.relation.tolist(), table2.colNames.index(joining_attr_t2))

    #print(sorted_t1)

    # Match the rows based on the joining attr
    size_check = len(sorted_t1) > len(sorted_t2)
    if size_check:
        result_table = Table(len(sorted_t2), len(sorted_t1[0]) + len(sorted_t2[0]) - 1)
        result_table.setColNames(table2.colNames)
        result_table.setColNames(table1.colNames)
        tempColNames = list(OrderedDict.fromkeys(result_table.colNames))
        result_table.colNames = []
        result_table.setColNames(tempColNames)
        #print(result_table.colNames)
        z = 0
        while z < result_table.numCols:
            result_table.relation[0,z] = result_table.colNames[z]
            z+=1

        i = 0
        while i < len(sorted_t2)-1: # Rows
            j = 0
            while j < len(sorted_t2[0]): # Cols
                result_table.relation[i+1,j] = sorted_t2[i][j]
                j+=1
            k = 0
            while k < len(sorted_t1[0]): # Cols
                if k != table1.colNames.index(joining_attr_t1):
                    result_table.relation[i+1,k+j-1] = sorted_t1[i][k]
                k+=1
            i+=1
        return result_table
    else:
        result_table = Table(len(sorted_t1), len(sorted_t1[0]) + len(sorted_t2[0]) - 1)
        result_table.setColNames(table1.colNames)
        result_table.setColNames(table2.colNames)
        tempColNames = list(OrderedDict.fromkeys(result_table.colNames))
        result_table.colNames = []
        result_table.setColNames(tempColNames)
        z = 0
        while z < result_table.numCols:
            result_table.relation[0,z] = result_table.colNames[z]
            z+=1

        i = 0
        while i < len(sorted_t1)-1: # Rows
            j = 0
            while j < len(sorted_t1[0]): # Cols
                result_table.relation[i+1,j] = sorted_t1[i][j]
                j+=1
            k = 0
            while k < len(sorted_t2[0]): # Cols
                if k != table2.colNames.index(joining_attr_t2):
                    result_table.relation[i+1,k+j-1] = sorted_t2[i][k]
                k+=1
            i+=1
        return result_table

def load_relations():
    # this works alright but waiting to talk with you about exactly what he wants
    database = Database()

    #*** Relation 1
    r1 = Table(101,2)
    r1.setName("Relation1")
    r1.setColNames(["col1", "col2"])

    np.put(r1.relation, 0, "col1")
    np.put(r1.relation, 1, "col2")

    for row in range(1,r1.numRows):
        for col in range(0,r1.numCols):
            np.put(r1.relation,row*r1.numCols+col,row)
    database.addRelation(r1)
    print(r1.relation)

    #*** Relation 2
    r2 = Table(1001,2)
    r2.setName("Relation2")

    np.put(r2.relation, 0, "col1")
    np.put(r2.relation, 1, "col3")
    r2.setColNames(["col1", "col3"])

    for row in range(1,r2.numRows):
        for col in range(0,r2.numCols):
            np.put(r2.relation,row*r2.numCols+col,row)
    database.addRelation(r2)
    # print(r2.relation)

    #*** Relation 3
    r3 = Table(101,2)
    r3.setName("Relation3")

    r3.relation.fill(1)
    np.put(r3.relation, 0, "col1")
    np.put(r3.relation, 1, "col4")
    r3.setColNames(["col1", "col4"])


    for row in range(1,r3.numRows):
        np.put(r3.relation, row*r3.numCols, row)
    database.addRelation(r3)
    # print(r3.relation)

    #*** Relation 4
    r4 = Table(1001,2)
    r4.setName("Relation4")

    r4.relation.fill(1)
    np.put(r4.relation, 0, "col1")
    np.put(r4.relation, 1, "col5")
    r4.setColNames(["col1", "col5"])

    for row in range(1,r4.numRows):
        np.put(r4.relation, row*r4.numCols, row)
    database.addRelation(r4)
    # print(r4.relation)

    #*** loads test relation
    index=0
    num_cols=3
    m=20
    cols = ["first","last","age"]
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
    columns = table.getColNames()
    np.put(table.relation,29,"jane")
    np.put(table.relation,30,"doe")
    np.put(table.relation,31,"3")
    np.put(table.relation,33,"greg")
    np.put(table.relation,34,"wills")
    np.put(table.relation,37,"donald")
    np.put(table.relation,38,"trump")
    # print(table.relation)
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
