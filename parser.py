# Database Management System Project
# COSC 280 - Georgetown University
# Greg Wills and David Wilke
# Professor Ophir Frieder

from eval import (
    eval_select,
    eval_delete,
    eval_create_table,
    eval_create_index,
    eval_drop_table,
    eval_drop_index,
    eval_insert,
    eval_update,
)
from table import *
from database import *


#######################################
# PARSE EXP ###########################
#######################################
def parse_expression(cmd, database):
    # takes in sql command in string form
    # returns a list of tokens

    # we don't necessarily want to tokenize just based on space because
    # a select statement can have a list of columns, we would wanna keep those
    # together, potentially on a list
    parseFlag = False
    quit = False
    index = 0
    begin = ""
    cols = []
    i = 0

    cmd = cmd.replace(";", "")  # drop semicolon from end of statement
    tokens = cmd.split(" ")  # split command by space
    tokens = [x.lower() for x in tokens]
    begin = tokens[i]

    if begin == "select":
        cols, tables, conditions, parseFlag = parse_select(i, tokens)
        if not parseFlag:
            eval_select(database, cols, tables, conditions)
    elif begin == "delete":
        for token in tokens:
            if token.lower() == "from":
                index = tokens.index(token)
        if not index:
            parseFlag = True  # missing from keyword in select statement
        else:
            table_name, conditions, i, parseFlag = parse_delete(index + 1, tokens)
            if not parseFlag:
                database = eval_delete(database, table_name, conditions)
    elif begin == "create":
        if tokens[i + 1] == "table":
            table_name, columns, types, parseFlag = create_table(tokens, i)
            if not parseFlag:
                database = eval_create_table(database, table_name, columns)
        elif tokens[i + 1] == "index":
            index_name, table_name, col_list, i, parseFlag = create_index(tokens, i + 2)
            if not parseFlag:
                eval_create_index(database, index_name, table_name, col_list)
    elif begin == "drop":
        if tokens[i + 1] == "table":
            table_name, i, parseFlag = drop_table(tokens, i)
            if not parseFlag:
                database = eval_drop_table(database, table_name)
        elif tokens[i + 1] == "index":
            dropped_index, table_ref, i, parseFlag = drop_index(tokens, i)
            if not parseFlag:
                eval_drop_index(database, dropped_index, table_ref)
    elif begin == "insert":
        if (
            tokens[i + 1] == "into"
        ):  # ASSUMPTION: only allowing for full tuples to be inserted
            table_name, values, parseFlag = parse_insert(tokens, i + 1)
            if not parseFlag:
                database = eval_insert(database, table_name, values)
        else:
            parseFlag = True
    elif begin == "update":
        table_name, col_vals, conditions, parseFlag = parse_update(tokens, i + 1)
        if not parseFlag:
            database = eval_update(database, table_name, col_vals, conditions)
    elif begin == "quit":
        print("Goodbye.")
    else:
        parseFlag = True

    if parseFlag:
        print("Encountered an error during parsing. Try again.")

    return database, tokens


#######################################
# PARSE SELECT ########################
#######################################
def parse_select(i, tokens):
    i += 1
    index = 0
    stripped_cols = []
    parseFlag = False
    is_distinct = False

    if tokens[i] == "distinct":
        is_distinct = True
        i += 1

    cols, i, parseFlag = parse_cols(i, tokens)
    # if parseFlag:
    #     return parseFlag
    tables, i, parseFlag = parse_table(i, tokens)
    # if parseFlag:
    #     return parseFlag
    conditions, i, parseFlag = parse_where(i, tokens)
    # if parseFlag:
    #     return parseFlag

    return cols, tables, conditions, parseFlag


#######################################
# PARSE COLUMNS #######################
#######################################
def parse_cols(i, tokens):
    parseFlag = False
    stripped_cols = []

    for token in tokens:
        if token == "from":
            index = tokens.index(token)
    cols = tokens[i:index]
    for col in cols:
        col = col.replace(",", "")
        stripped_cols.append(col)
    cols = stripped_cols
    if not cols:
        parseFlag = True
    # else:
    #     print("Columns to select: ", cols)
    return cols, index, parseFlag


#######################################
# PARSE TABLE #########################
#######################################
def parse_table(i, tokens):
    i += 1
    where_index = 0
    tuple_list = []
    parseFlag = False

    for token in tokens:
        if token == "where":
            where_index = tokens.index(token)
    if where_index == 0:
        where_index = len(tokens)
    table_info = tokens[i:where_index]
    table_info = " ".join(table_info)
    table_list = table_info.split(", ")

    if len(table_list) == 1:  # Handle one table situation
        temp = table_list[0].split(" ")
        if temp == table_list:
            tuple_list.append(table_list[0])
        else:
            tuple_list.append((temp[0], temp[1]))
    else:  # ASSUMPTION: Tables have aliases
        for tok in table_list:
            temp = tok.split(" ")
            if len(temp) == 2:
                name_and_alias = (temp[0], temp[1])
                tuple_list.append(name_and_alias)
            else:
                parseFlag = True

    i = where_index
    return tuple_list, i, parseFlag


#######################################
# PARSE WHERE #########################
#######################################
def parse_where(i, tokens):
    i += 1  # this is now just past the where
    parseFlag = False
    conditions = []
    end_of_where = len(tokens)  # Assumption: where clause is the last thing in a query

    if i >= end_of_where:
        return conditions, i, parseFlag

    where_conditions = tokens[i:end_of_where]
    # print(where_conditions)
    split_list = ["and", "or"]  # list of valid splitting tokens
    split_indicies = []  # list of indicies to split conditions on
    for cond_index in range(len(where_conditions)):
        if where_conditions[cond_index] in split_list:
            split_indicies.append(cond_index)

    split_indicies.append(len(where_conditions))

    # There could also be parenthesis in here which determine Order of Operations
    # Start by assuming there are none
    # TODO: Handle an "and" as part of a between clause
    start_index = 0
    for end_index in split_indicies:
        temp_list = where_conditions[start_index:end_index]
        # print("Temp list: " + str(temp_list))
        if len(temp_list) == 3:
            condition_tuple = tuple(temp_list)
            conditions.append(condition_tuple)
        elif (
            temp_list[0] in split_list
        ):  # assuming the first thing is a splitting token
            condition_tuple = temp_list[0]
            conditions.append(condition_tuple)
            condition_tuple2 = tuple(temp_list[1:])
            conditions.append(condition_tuple2)
        else:
            condition_tuple = tuple(temp_list)
            conditions.append(condition_tuple)
        start_index = end_index

    # print("Where Conditions: " , conditions)
    return conditions, i, parseFlag


#######################################
# PARSE DELETE ########################
#######################################
def parse_delete(i, tokens):
    parseFlag = False
    temp_name = tokens[i]
    conditions = []
    if temp_name[len(temp_name) - 2] == ";" or i + 1 == len(tokens):
        table_name = temp_name[:-1]
    else:
        table_name = tokens[i]  # ASSUMPTION: Only one table
        conditions, i, parseFlag = parse_where(i + 1, tokens)
    return table_name, conditions, i, parseFlag


#######################################
# CREATE TABLE ########################
#######################################
def create_table(tokens, i):
    print(tokens)
    error = False
    i += 2
    columns = []
    types = []
    table_name = tokens[i]
    # tokens.remove(table_name)
    i += 1
    values = " ".join(tokens[i:])
    val_and_col = values.split(", ")
    for token in val_and_col:
        token = token.replace("(", "")
        token = token.replace(")", "")
        token = token.replace(",", "")

        test = token.split(" ")
        columns.append(test[0])
        if len(test) == 2:
            types.append(test[1])
        else:
            error = True
    # print(columns)

    # succesfully grabs the columns and values to be added to new table
    if not error:
        print(table_name.upper() + " table succesfully created.")
    else:
        print("Error in creating table " + table_name.upper() + ".")
        print("Encountered parse error.")

    return table_name, columns, types, error


#######################################
# DROP TABLE ##########################
#######################################
def drop_table(tokens, i):
    if_exists = False
    table_name = ""
    i += 2
    parseError = False

    if len(tokens[i:]) == 1:
        if_exists = False
    elif len(tokens[i:]) == 3:
        if tokens[i] == "if" and tokens[i + 1] == "exists":
            if_exists = True  # check if table exists
            i += 2
    else:
        parseError = True
    table_name = tokens[i].replace(";", "")

    # if table_name exists, drop it
    if not parseError:
        placeholder = True
        # print(table_name.upper() + " table successfully deleted.")
    else:
        print("Error in deleting table " + table_name.upper() + ".")

    return table_name, i, parseError


#######################################
# DROP INDEX ##########################
#######################################
def drop_index(tokens, i):
    parseError = False
    index_name = ""
    table_ref = ""
    is_exists = True
    i += 2

    if len(tokens[i:]) > 2:
        if tokens[i] == "if" and tokens[i + 1] == "exists":
            is_exists = True  # Check if index exists
            i += 2
    else:
        parseError = True
    index_name, table_ref, i, parseError = parse_drop_index(tokens, i)

    # print(index_name + " , " + table_ref)

    return index_name, table_ref, i, parseError


def parse_drop_index(tokens, i):
    parseError = False
    index_name = tokens[i]
    i += 1
    if tokens[i] == "on":
        i += 1
        table_ref = tokens[i]
    else:
        parseError = True
    return index_name, table_ref, i, parseError


#######################################
# CREATE INDEX ########################
####################################### TODO: Fix error of cols not being accepted
def create_index(tokens, i):
    parseError = False
    if tokens[i] == "if" and tokens[i + 1] == "not":
        ifNotExistsCheck = True
        i += 3
    index_name = tokens[i]
    i += 1
    # Sanity check
    if tokens[i] == "on":
        table_name = tokens[i + 1]  # ASSUMPTION: parens are not own tokens
        column_list = []
        temp_vals = tokens[i + 2 :]
        for tok in temp_vals:
            new_tok = tok
            if "(" in tok:
                new_tok = new_tok.replace("(", "")
            if ")" in tok:
                new_tok = new_tok.replace(")", "")
            if "," in tok:
                new_tok = new_tok.replace(",", "")
            column_list.append(new_tok)

        return index_name, table_name, column_list, i, parseError
    else:
        return index_name, "", [], i, True


#######################################
# INSERT INTO #########################
#######################################


def parse_insert(tokens, i):
    parseError = False
    table_name = tokens[i + 1]
    values = []

    # move i beyond the values keyword
    i += 3

    temp_vals = tokens[i:]
    for tok in temp_vals:
        new_tok = tok
        if "(" in tok:
            new_tok = new_tok.replace("(", "")
        if ")" in tok:
            new_tok = new_tok.replace(")", "")
        if "," in tok:
            new_tok = new_tok.replace(",", "")
        values.append(new_tok)

    return table_name, values, parseError


def parse_update(tokens, i):
    parseError = False
    table_name = tokens[i]
    col_vals = []

    i += 2  # move the tokens past the set token
    try:
        end_of_tuples = tokens.index("where")
    except:
        j = 0
        col_val_conditions = tokens[i:]
        while j <= len(col_val_conditions) - 3:
            tuple = (
                col_val_conditions[j],
                col_val_conditions[j + 1],
                col_val_conditions[j + 2],
            )
            if not tuple:
                parseError = True
                j = len(col_val_conditions) - 3
            else:
                col_vals.append(tuple)
                j += 3
        return table_name, col_vals, [], parseError

    col_val_conditions = tokens[i:end_of_tuples]
    # print(col_val_conditions)

    # iterate through the conditions, putting every trio in a tuple
    j = 0
    while j <= len(col_val_conditions) - 3:
        tuple = (
            col_val_conditions[j],
            col_val_conditions[j + 1],
            col_val_conditions[j + 2].replace(",", ""),
        )
        # print(tuple)
        if not tuple:
            parseError = True
            j = len(col_val_conditions) - 3
        else:
            col_vals.append(tuple)
            j += 3
    # print(col_vals)
    if not parseError:
        i = end_of_tuples
        conditions, i, parseError = parse_where(i, tokens)
        return table_name, col_vals, conditions, parseError
    else:
        return table_name, col_vals, [], parseError
