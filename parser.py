# testing command prompt

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
    statement_length = len(tokens)

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
            drop_table = True
            print("drop table is true")
            print("tokens being passed in: ", tokens[2:])

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
    columns = []
    vals = []
    table_name = tokens[0]
    tokens.remove(table_name)
    tokens = ' '.join(tokens)
    print(tokens)
    val_and_col = tokens.split(", ")
    print(val_and_col)
    for token in val_and_col:
        token = token.replace('(','')
        token = token.replace(')','')
        token = token.replace(',','')

        test = token.split(' ')
        columns.append(test[0])
        vals.append(test[1])

    print("columns: ", columns)
    print("values: ", vals)

    # succesfully grabs the columns and values to be added to new table
    print(table_name.upper() + " table succesfully created.")


def evaluator(token_list):
    # takes in list of tokens in List form
    # checks for SQL statement validity based on SQL grammar

    return True

def main():
    cmd = ""
    prompt = "> "
    while cmd != "quit":
        cmd = raw_input(prompt)
        tokens = tokenizer(cmd)
        # print tokens


main()
