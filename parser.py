# Database Management System Project
# COSC 280 - Georgetown University
# Greg Wills and David Wilke
# Professor Ophir Frieder

def tokenizer(cmd):
    # takes in sql command in string form
    # returns a list of tokens

    # we don't necessarily want to tokenize just based on space because
    # a select statement can have a list of columns, we would wanna keep those
    # together, potentially on a list
    parseFlag = False
    index = 0
    cols = []

    tokens = cmd.split(" ")

    if tokens[0].lower() == "select":
        for token in tokens:
            if token.lower() == "from":
                index = tokens.index(token)
        cols = tokens[1:index]
        stripped_cols = []
        for col in cols:
            col = col.replace(',','')
            stripped_cols.append(col)
        cols = stripped_cols
        if not cols:
            parseFlag = True
        else:
            print("Columns to select: ", cols)
    elif tokens[0].lower() == "delete":
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
    elif (tokens[0].lower() == "create"):
        if tokens[1].lower() == "table":
            create_table(tokens[2:])
        elif tokens[1].lower() == "index":
            create_index = True
    elif (tokens[0].lower() == "drop"):
        if tokens[1].lower() == "table":
            drop_table(tokens[2:])
        elif tokens[1].lower() == "index":
            drop_index = True
    elif tokens[0].lower() == "quit":
        print("Goodbye")
    else:
        parseFlag = True

    if parseFlag:
        print("Encountered an error during parsing. Try again.")


    eval = evaluator(tokens)
    return tokens

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


def evaluator(token_list):
    # takes in list of tokens in List form
    # checks for SQL statement validity based on SQL grammar
    # ASSUMPTION: the passed in list is all in lowercase
    result = True
    valid_begin = ["select", "create", "drop", "insert", "update", "delete"]
    begin = token_list.pop(0)
    if (begin in valid_begin):
    	# Need some form of recusion here?
    	if (begin == "select"):
    		# Go to select specific eval?
    		result = True # temporary
    else:
    	result = False


    return result

def main():
    cmd = ""
    prompt = "> "
    while cmd.lower() != "quit":
        cmd = raw_input(prompt)
        tokens = tokenizer(cmd)
        # print tokens


main()
