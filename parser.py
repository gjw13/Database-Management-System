# testing command prompt

def tokenizer(cmd):
    # takes in sql command in string form
    # returns a list of tokens
    tokens = cmd.split(" ")
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


main()
