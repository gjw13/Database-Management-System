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
            create_table = True
        elif tokens[1].lower() == "index":
            create_index = True
    elif (tokens[0].lower() == "drop"):
        if tokens[1].lower() == "table":
            drop_table = True
        elif tokens[1].lower() == "index":
            drop_index = True
    else:
        parseFlag = True

    if tokens[0] == "quit":
        print("Goodbye")
    if parseFlag:
        print("Encountered an error during parsing. Try again.")


    eval = evaluator(tokens)
    return tokens

def evaluator(token_list):
    # takes in list of tokens in List form
    # checks for SQL statement validity based on SQL grammar

    return True

def main():
    cmd = ""
    while cmd != "quit":
        cmd = raw_input("> ")
        tokens = tokenizer(cmd)
        # print tokens


main()
