# Database Management System Project
# COSC 280 - Georgetown University
# Greg Wills and David Wilke
# Professor Ophir Frieder

import eval

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


    tokens = cmd.split(" ")
    tokens = [x.lower() for x in tokens]
    begin = tokens[i]

    if begin == "select":
        parse_select(i,tokens)
    elif begin == "delete":
        for token in tokens:
            if token.lower() == "from":
                index = tokens.index(token)
        if not index:
            parseFlag = True # missing from keyword in select statement
        else:
            cols = tokens[1:index]
            stripped_cols = []
            for col in cols:
                col = col.replace(',','')
                stripped_cols.append(col)
                cols = stripped_cols
            if not cols:
                parseFlag = True
            else:
                print("Columns to delete: ", cols)
    elif begin == "create":
        if tokens[1].lower() == "table":
            create_table(tokens[2:])
        elif tokens[1].lower() == "index":
            create_index = True
    elif begin == "drop":
        if tokens[1].lower() == "table":
            drop_table(tokens[2:])
        elif tokens[1].lower() == "index":
            drop_index = True
    elif begin == "quit":
        print("Goodbye.")
    else:
        parseFlag = True

    if parseFlag:
        print("Encountered an error during parsing. Try again.")


    eval = evaluator(tokens)
    return tokens

def parse_select(i,tokens):
    i+=1
    index=0
    stripped_cols = []
    parseFlag = False

    cols, index, parseFlag = parse_cols(i,tokens)
    i=index
    tables, i, parseFlag = parse_table(i,tokens)

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
    for tok in table_list:
        temp = tok.split(" ")
        if len(temp) == 2:
            name_and_alias = (temp[0],temp[1])
            tuple_list.append(name_and_alias)
        else:
            parseFlag = True
    return tuple_list, i, parseFlag

def parse_where(i, tokens):
    i+=1
    parseFlag = False


def create_table(tokens):
    error = False
    columns = []
    types = []
    table_name = tokens[0]
    tokens.remove(table_name)
    tokens = ' '.join(tokens)
    val_and_col = tokens.split(", ")
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

    # succesfully grabs the columns and values to be added to new table
    if not error:
        print(table_name.upper() + " table succesfully created.")
    else:
        print("Error in creating table " + table_name.upper() + ".")

def drop_table(tokens):
    error = False
    print(tokens)
    if tokens:
        table_name = tokens[0]
    else:
        error = True
    # if table_name exists, drop it
    if not error:
        print(table_name.upper() + " table successfully deleted.")
    else:
        print("Error in deleting table " + table_name.upper() + ".")


def main():
    cmd = ""
    prompt = "> "
    while cmd.lower() != "quit":
        cmd = raw_input(prompt)
        tokens = parse_expression(cmd)
        # print tokens


main()
