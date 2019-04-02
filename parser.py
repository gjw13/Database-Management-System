# Database Management System Project
# COSC 280 - Georgetown University
# Greg Wills and David Wilke
# Professor Ophir Frieder

# import eval

#######################################
# PARSE EXP ###########################
#######################################
def parse_expression(cmd):
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
    i=0

    # drop semicolon from end of statement

    tokens = cmd.split(" ")
    tokens = [x.lower() for x in tokens]
    begin = tokens[i]

    if begin == "select":
        parseFlag = parse_select(i,tokens) # Need to add some other return array here to send to eval
    elif begin == "delete":
        for token in tokens:
            if token.lower() == "from":
                index = tokens.index(token)
        if not index:
            parseFlag = True # missing from keyword in select statement
        else:
            parse_delete(index+1, tokens)
    elif begin == "create":
        if tokens[i+1] == "table":
            create_table(tokens,i)
        elif tokens[i+1] == "index":
            create_index(tokens, i+2)
    elif begin == "drop":
        if tokens[i+1] == "table":
            table_name,i = drop_table(tokens,i)
        elif tokens[i+1] == "index":
            dropped_index,table_ref,i = drop_index(tokens,i)
    elif begin == "quit":
        print("Goodbye.")
    else:
        parseFlag = True

    if parseFlag:
        print("Encountered an error during parsing. Try again.")

    return tokens

#######################################
# PARSE SELECT ########################
#######################################
def parse_select(i,tokens):
    i+=1
    index=0
    stripped_cols = []
    parseFlag = False
    is_distinct = False

    if tokens[i] == "distinct":
        is_distinct = True
        i+=1

    cols, i, parseFlag = parse_cols(i,tokens)
    if (parseFlag):
        return parseFlag
    tables, i, parseFlag = parse_table(i,tokens)
    if (parseFlag):
        return parseFlag
    conditions, i, parseFlag = parse_where(i,tokens)
    if (parseFlag):
        return parseFlag

    return parseFlag # Need to add some other return array here to send to eval

#######################################
# PARSE COLUMNS #######################
#######################################
def parse_cols(i,tokens):
    parseFlag = False
    stripped_cols = []

    for token in tokens:
        if token == "from":
            index = tokens.index(token)
    cols = tokens[i:index]
    for col in cols:
        col = col.replace(',','')
        stripped_cols.append(col)
    cols = stripped_cols
    if not cols:
        parseFlag = True
    else:
        print("Columns to select: ", cols)
    return cols, index, parseFlag

#######################################
# PARSE TABLE #########################
#######################################
def parse_table(i,tokens):
    i+=1
    where_index=0
    tuple_list = []
    parseFlag = False

    for token in tokens:
        if token == "where":
            where_index = tokens.index(token)
    if where_index == 0:
        where_index = len(tokens)
    table_info = tokens[i:where_index]
    table_info = ' '.join(table_info)
    table_list = table_info.split(", ")

    if (len(table_list) == 1): # Handle one table situation
        tuple_list.append(table_list[0])
    else:
        for tok in table_list:
            temp = tok.split(" ")
            if len(temp) == 2:
                name_and_alias = (temp[0],temp[1])
                tuple_list.append(name_and_alias)
            else:
                parseFlag = True

    i = where_index
    print("Tables selected from: " , tuple_list)
    return tuple_list, i, parseFlag

#######################################
# PARSE WHERE #########################
#######################################
def parse_where(i, tokens):
    i+=1 #this is now just past the where
    parseFlag = False
    conditions = []
    end_of_where = len(tokens) # Assumption: where clause is the last thing in a query


    where_conditions = tokens[i:end_of_where]
    print(where_conditions)
    split_list = ["and", "or", "in", "like", "between"] # list of valid splitting tokens TODO: NOT
    split_indicies = [] # list of indicies to split conditions on
    for tok in where_conditions:
        if tok in split_list:
            split_indicies.append(where_conditions.index(tok))

    split_indicies.append(len(where_conditions))
    print(split_indicies)
    # There could also be parenthesis in here which determine Order of Operations
    # Start by assuming there are none
    start_index = 0
    for end_index in split_indicies:
        temp_list = where_conditions[start_index:end_index]
        if len(temp_list) == 3:
            condition_tuple = (temp_list[0], temp_list[1], temp_list[2])
            conditions.append(condition_tuple)
        elif len(temp_list) == 4: #assuming the first thing is a splitting token
            condition_tuple = (temp_list[0])
            conditions.append(condition_tuple)
            condition_tuple2 = (temp_list[1], temp_list[2], temp_list[3])
            conditions.append(condition_tuple2)
        else:
            parseFlag = True
        start_index = end_index

    print("Where Conditions: " , conditions)
    return conditions, i, parseFlag


#######################################
# PARSE DELETE ########################
#######################################
def parse_delete (i, tokens):
    parseFlag = False
    temp_name = tokens[i]
    if temp_name[len(temp_name)-2] == ";" or i+1 == len(tokens):
        table_name = temp_name[:-1]
        return table_name, i, parseFlag
    else:
        table_name = tokens[i]
        conditions, i, parseFlag = parse_where(i+1, tokens)
        return table_name, conditions, i, parseFlag


#######################################
# CREATE TABLE ########################
#######################################
def create_table(tokens,i):
    error = False
    i+=2
    columns = []
    types = []
    table_name = tokens[i]
    # tokens.remove(table_name)
    i+=1
    values = ' '.join(tokens[i:])
    val_and_col = values.split(", ")
    for token in val_and_col:
        token = token.replace('(','')
        token = token.replace(')','')
        token = token.replace(',','')

        test = token.split(' ')
        columns.append(test[0])
        if len(test) == 2:
            types.append(test[1])
        else:
            error = True
    print(columns)

    # succesfully grabs the columns and values to be added to new table
    if not error:
        print(table_name.upper() + " table succesfully created.")
    else:
        print("Error in creating table " + table_name.upper() + ".")
        print("Encountered parse error.")

#######################################
# DROP TABLE ##########################
#######################################
def drop_table(tokens,i):
    if_exists = False
    table_name = ""
    i+=2
    if len(tokens[i:])==1:
        if_exists = False
    elif len(tokens[i:])==3:
        if tokens[i]=="if" and tokens[i+1]=="exists":
            if_exists = True # check if table exists
            i+=2
    else:
        parseError = True
    table_name = tokens[i].replace(';','')

    # if table_name exists, drop it
    if not parseError:
        print(table_name.upper() + " table successfully deleted.")
    else:
        print("Error in deleting table " + table_name.upper() + ".")

    return table_name,i


#######################################
# DROP INDEX ##########################
#######################################
def drop_index(tokens,i):
    parseError = False
    index_name = ""
    table_ref = ""
    is_exists = True
    i+=2

    if len(tokens[i:])>2:
        if tokens[i] == "if" and tokens[i+1] == "exists":
            is_exists = True #check if index exists
            i+=2
    else:
        parseError = True
    index_name,table_ref,i = parse_drop_index(tokens,i)

    # print(index_name + " , " + table_ref)

    return index_name,table_ref,i

def parse_drop_index(tokens,i):
    parseError = False
    index_name = tokens[i]
    i+=1
    if tokens[i] == "on":
        i+=1
        table_ref = tokens[i]
    else:
        parseError = True
    return index_name,table_ref,i



#######################################
# CREATE INDEX ########################
#######################################
def create_index(tokens, i):
    parseError = False
    if (tokens[i] == "if" and tokens[i+1] == "not"):
        ifNotExistsCheck = True
        i+=3
    index_name = tokens[i]
    i+=1
    # Sanity check
    if tokens[i] == "on":
        table_name = tokens[i+1] # ASSUMPTION: all parens are seperated by spaces on both sides
        column_list = []
        if (tokens[i+2] == "("):
            end_of_col_index = tokens.index(")", i+2)
            i+=3
            while (i < end_of_col_index):
                col_name = tokens[i]
                i+=1
                temp_order = tokens[i]
                if temp_order[len(temp_order)-2] == ",":
                    ordering = temp_order[:-1]
                else:
                    ordering = tokens[i]
                column_list.append((col_name, ordering))
                i+=1
        # ASSUMPTION: No "include" block afterwards
        print(column_list)
        return column_list, i, parseError
    else:
        return i, True

def main():
    cmd = ""
    prompt = "> "
    while cmd != "quit":
        cmd = raw_input(prompt)
        tokens = parse_expression(cmd)
        # print tokens


main()
